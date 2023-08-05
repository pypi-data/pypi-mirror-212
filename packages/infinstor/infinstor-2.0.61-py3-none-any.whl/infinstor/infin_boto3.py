from datetime import datetime, timezone
import builtins
from typing import List, Tuple
import boto3
from botocore.response import StreamingBody
from botocore.exceptions import ClientError
from botocore.response import StreamingBody
import functools
import os
import sys
from os.path import expanduser
import json
import time
import re
import mlflow
from mlflow.tracking import MlflowClient
from urllib.parse import urlparse, quote
from requests.exceptions import HTTPError
import requests
import infinstor
from infinstor import bootstrap, tokenfile
import xmltodict
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import urllib3
import traceback

#from http.client import HTTPConnection
#HTTPConnection.debuglevel = 2

connection_pools = {}
user_info_cache = {}

def _log_urllib3_Response(resp:urllib3.response.HTTPResponse):
    print(f"urllib3.request.method= urllib3.response.geturl()={resp.geturl()}")
    print(f"urllib3.response.headers={resp.getheaders()}")
    if resp.data: print(f"urllib3.response.data (truncated < 1024)={resp.data if len(resp.data) < 1024 else resp.data[:1024]}")
    
def _log_requests_Response(resp:requests.Response):
    print(f"response.request.method={resp.request.method} response.request.url={resp.request.url}")
    print(f"response.request.headers={resp.request.headers}")
    if resp.request.body: print(f"response.request.body (truncated < 1024)={resp.request.body if len(resp.request.body) < 1024 else resp.request.body[:1024]}")
    print(f"response.status_code={resp.status_code}")
    print(f"response.headers={resp.headers}")
    if resp.content: print(f"response.content (truncated < 1024)={resp.content if len(resp.content) < 1024 else resp.content[:1024]}")
    
class InfinStreamingBody(StreamingBody):
    def __init__(self, raw_stream, content_length):
        super(InfinStreamingBody, self).__init__(raw_stream, content_length)
        self.rs = raw_stream

    def __del__(self):
        self.rs.drain_conn()

def parse_run_id(prefix):
    #match pattern like /22/22-16547558543270000000139/
    if not prefix:
        return None
    run_id = None
    m = re.match("^.*\/(\d+)\/(\d+)-(\d{23})(\/|$)", prefix)
    if m:
        groups = m.groups()
        if groups and len(groups) >= 3 and groups[0] == groups[1] and len(groups[2]) == 23:
            run_id = groups[1] + '-' + groups[2]
    return run_id


class ListObjectsPaginator():
    def __init__(self, type2, infin_boto_client, infinsnap_buckets = [],
                 non_infinsnap_buckets = [], concurrent_user_buckets = []):
        self.type2 = type2
        self.infin_boto_client = infin_boto_client
        self.infinsnap_buckets = infinsnap_buckets
        self.non_infinsnap_buckets = non_infinsnap_buckets
        self.concurrent_user_buckets = concurrent_user_buckets
        self.all_buckets = infinsnap_buckets + non_infinsnap_buckets + concurrent_user_buckets
        self.next_token = None
        self.finished = False

    def paginate(self, **kwargs):
        if 'Bucket' not in kwargs:
            raise ValueError("Bucket must be specified for list-objects-v2 paginate")
        self.bucket = kwargs['Bucket']
        self.prefix = kwargs.get('Prefix')
        run_id = parse_run_id(self.prefix)
        if not run_id and self.bucket not in self.all_buckets:
            print('No run_id and unknown bucket {}, use default client'.format(self.bucket))
            passthru = self.infin_boto_client.defaultClient.get_paginator('list_objects_v2')
            return passthru.paginate(**kwargs)
        else:
            self.kwargs = kwargs
            return self

    def __iter__(self):
        return self
    def __next__(self):
        if self.finished:
            raise StopIteration
        if (self.next_token):
            if self.type2:
                self.kwargs['ContinuationToken'] = self.next_token
            else:
                self.kwargs['Marker'] = self.next_token
        if self.type2:
            rv = self.infin_boto_client.list_objects_v2(None, **self.kwargs)
            if 'NextContinuationToken' in rv:
                self.next_token = rv['NextContinuationToken']
                del rv['NextContinuationToken']
            else:
                self.finished = True
            return rv
        else:
            rv = self.infin_boto_client.list_objects(None, **self.kwargs)
            if 'NextMarker' in rv:
                self.next_token = rv['NextMarker']
                del rv['NextMarker']
            else:
                self.finished = True
            return rv

class Bucket():
    def __init__(self, name):
        self.name = name

class BucketsCollection():
    def __init__(self, infinsnap_buckets, non_infinsnap_buckets):
        self._infinsnap_buckets = [Bucket(b) for b in infinsnap_buckets]
        self._non_infinsnap_buckets = [Bucket(b) for b in non_infinsnap_buckets]
    def all(self):
        return self._infinsnap_buckets + self._non_infinsnap_buckets
    def infinsnap_buckets(self):
        return self._infinsnap_buckets
    def non_infinsnap_buckets(self):
        return self._non_infinsnap_buckets

class S3ResourceMeta():
    def __init__(self, default_meta, infin_client):
        self.default_meta = default_meta
        self.infin_client = infin_client
    def __getattr__(self, attr):
        if attr == 'client':
            return self.infin_client
        else:
            return getattr(self.default_meta, attr)

class InfinBotoResource():
    def __init__(self, defaultResource, timespec_info):
        self.defaultResource = defaultResource
        self.timespec_info = timespec_info
        self.bucketscollection = BucketsCollection(timespec_info['infinsnap_buckets'], timespec_info['non_infinsnap_buckets'])
        self.s3_resource_meta = S3ResourceMeta(self.defaultResource.meta,
                InfinBotoClient(defaultResource.meta.client, timespec_info))

    def __getattr__(self, attr):
        if attr == 'buckets':
            return self.bucketscollection
        elif attr == 'meta':
            return self.s3_resource_meta
        else:
            return getattr(self.defaultResource, attr)

class InfinBotoClient():
    def __init__(self, defaultClient, timespec_info):
        # self.__class__ = type(baseObject.__class__.__name__,
        #                       (self.__class__, baseObject.__class__),
        #                       {})
        # self.__dict__ = baseObject.__dict__
        self.defaultClient = defaultClient
        self.timespec_info = timespec_info
        self.bucket = None
        self.prefix = None
        self.have_printed_greeting = False

    def list_objects(self, *args, **kwargs):
        if self.timespec_info['type'] == 'infinsnap' or self.timespec_info['type'] == 'infinslice' or 'time_spec' in self.timespec_info:
            if self.bucket:
                request_bucket = self.bucket
                request_prefix = self.prefix
            elif kwargs['Bucket']:
                request_bucket = kwargs['Bucket']
                request_prefix = kwargs['Prefix']
            else:
                raise ValueError("bucket must be specified")
            if request_bucket in self.timespec_info['infinsnap_buckets']:
                kwargs['Bucket'] = request_bucket
                kwargs['Prefix'] = request_prefix
                return self.list_objects_at(False, *args, **kwargs)
            elif request_bucket in self.timespec_info['concurrent_user_buckets']:
                return self.list_objects_presigned(request_bucket, request_prefix, None, **kwargs)
            #elif request_bucket in self.timespec_info['non_infinsnap_buckets']:
            else:
                kwargs['Bucket'] = request_bucket
                kwargs['Prefix'] = request_prefix
                run_id = parse_run_id(request_prefix)
                if run_id:
                    return self.list_objects_presigned(request_bucket, request_prefix, run_id, **kwargs)
                else:
                    return self.defaultClient.list_objects(**kwargs)
            # else:
            #     return self.defaultClient.list_objects(**kwargs)
        else:
            return self.defaultClient.list_objects(**kwargs)

    def print_greeting(self, context):
        if not self.have_printed_greeting:
            try:
                print('infin_boto3:' + str(context) +' intercept activated for buckets='
                    + str(self.timespec_info['infinsnap_buckets']
                          + self.timespec_info['non_infinsnap_buckets']
                          + self.timespec_info['concurrent_user_buckets']))
            except Exception as ex:
                pass
            self.have_printed_greeting = True

    def to_json_response(self, response:requests.Response, content_key):
        if not response.ok: _log_requests_Response(response)
        respj = xmltodict.parse(response.content)
        respj = respj[content_key]
        if 'Contents' in respj:
            if type(respj['Contents']) != list:
                respj['Contents'] = [respj['Contents']]

        if 'CommonPrefixes' in respj:
            if type(respj['CommonPrefixes']) != list:
                respj['CommonPrefixes'] = [respj['CommonPrefixes']]

        return respj


    def list_objects_v2(self, *args, **kwargs):
        self.print_greeting("list_objects_v2")
        if self.timespec_info['type'] == 'infinsnap' or self.timespec_info['type'] == 'infinslice' or 'time_spec' in self.timespec_info:
            if self.bucket:
                request_bucket = self.bucket
                request_prefix = self.prefix
            elif kwargs['Bucket']:
                request_bucket = kwargs['Bucket']
                request_prefix = kwargs['Prefix']
            else:
                raise ValueError("bucket must be specified")
            if request_bucket in self.timespec_info['infinsnap_buckets']:
                kwargs['Bucket'] = request_bucket
                kwargs['Prefix'] = request_prefix
                return self.list_objects_at(True, *args, **kwargs)
            elif request_bucket in self.timespec_info['concurrent_user_buckets']:
                return self.list_objects_v2_presigned(request_bucket, request_prefix, None, **kwargs)
            #elif request_bucket in self.timespec_info['non_infinsnap_buckets']:
            else:
                kwargs['Bucket'] = request_bucket
                kwargs['Prefix'] = request_prefix
                run_id = parse_run_id(request_prefix)
                if run_id:
                    return self.list_objects_v2_presigned(request_bucket, request_prefix, run_id, **kwargs)
                else:
                    return self.defaultClient.list_objects_v2(**kwargs)
        else:
            return self.defaultClient.list_objects_v2(**kwargs)

    def download_file_presigned(self, ps_url, fname):
        parsed_url = urlparse(ps_url)
        if parsed_url.hostname in connection_pools:
            print(f'download_file_presigned: hostname={parsed_url.hostname} is in pool cache')
            pool = connection_pools[parsed_url.hostname]
        else:
            print(f'download_file_presigned: hostname={parsed_url.hostname} is NOT in pool cache')
            pool = urllib3.HTTPSConnectionPool(parsed_url.hostname)
            connection_pools[parsed_url.hostname] = pool
        try:
            response = pool.request('GET', ps_url, preload_content=False, timeout=urllib3.Timeout(connect=5.0, read=10.0), retries=urllib3.Retry(3, redirect=2))
        except HTTPError as http_err:
            traceback.print_exc()
            if http_err.response.status_code == 404: # not found
                print(f"download_file_presigned: pool.request({ps_url}) returned error 404 {http_err}. Throwing botocore exception instead")
                raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, 'download_file')
        except Exception as ex:
            traceback.print_exc()
            print(f"download_file_presigned: pool.request threw {ex}")
            raise
        if response.status == 404:
            _log_urllib3_Response(response)
            print(f"download_file_presigned: pool.request returned status 404. Throwing botocore exception instead")
            raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, 'download_file')
        elif response.status == 403:
            _log_urllib3_Response(response)
            raise Exception('Access Denied')
        clen = response.getheader('Content-Length')
        isb = InfinStreamingBody(response, clen)
        with open(fname, 'wb') as fp:
            while True:
                chunk = isb.read(64*1024)
                if not chunk:
                    break
                fp.write(chunk)
        print(f'download_file_presigned: download to {fname} complete')
        return

    def download_file(self, *args, **kwargs):
        if self.timespec_info['type'] == 'infinsnap' or self.timespec_info['type'] == 'infinslice' or 'time_spec' in self.timespec_info:
            request_bucket = args[0]
            request_file = args[1]
            if request_bucket in self.timespec_info['infinsnap_buckets']:
                versionId, ps_url = self.get_version_id(request_bucket, request_file, 'download_file')
                if (versionId != None):
                    if self.timespec_info['use_presigned_url_for_infinsnap']:
                        print(f"infin_boto3.download_file({request_bucket}, {request_file}). is infinsnap bucket. using ps_url", flush=True)
                        self.download_file_presigned(ps_url, args[2])
                        return
                    else:
                        if 'ExtraArgs' in kwargs:
                            kwargs['ExtraArgs']['VersionId'] = versionId
                        else:
                            kwargs['ExtraArgs'] = {'VersionId': versionId}
                        print(f"infin_boto3.download_file({request_bucket}, {request_file}). not configured with ps_url for infinsnap. sending to default", flush=True)
                        return self.defaultClient.download_file(*args, **kwargs)
                else:
                    raise ValueError('download_file: versionId not present. Is InfinSnap enabled?')
            elif request_bucket in self.timespec_info['concurrent_user_buckets']:
                ps_url = self.get_presigned_url(request_bucket, request_file, None, 'get_object')
                print(f"infin_boto3.download_file({request_bucket}, {request_file}). is user bucket. using ps_url", flush=True)
                self.download_file_presigned(ps_url, args[2])
                return
            else:
                run_id = parse_run_id(request_file)
                if run_id:
                    ps_url = self.get_presigned_url(request_bucket, request_file, run_id, 'get_object')
                    print(f"infin_boto3.download_file({request_bucket}, {request_file}). is mlflow artifact. using ps_url", flush=True)
                    self.download_file_presigned(ps_url, args[2])
                    return
                else:
                    print(f"infin_boto3.download_file({request_bucket}, {request_file}). not a mlflow artifact. sending to default", flush=True)
                    self.defaultClient.download_file(*args, **kwargs)
                    return
        else:
            print(f"infin_boto3.download_file({request_bucket}, {request_file}). no timespec. sending to default", flush=True)
            self.defaultClient.download_file(*args, **kwargs)
            return

    def get_auth_header(self, force=False):
        token = tokenfile.get_token(builtins.region, force)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': token
        }
        return headers

    def get_version_id(self, bucket, prefix, caller_name) -> Tuple[str,str]:
        """
        returns the version_id and presigned url for the specified bucket/prefix

        Args:
            bucket (str): bucket name
            prefix (str): prefix in the bucket
            caller_name (str): the name of the caller of this function: download_file, get_object, head_object, etc

        Raises:
            ClientError: _description_

        Returns:
            Tuple[str,str]: returns the tuple (version_id, presigned url)
        """
        attempt = 0
        while attempt < 2:
            if attempt == 0:
                force = False
            else:
                print('get_version_id: attempt = ' + str(attempt) + ', force True')
                force = True
            attempt = attempt + 1
            token = tokenfile.get_token(builtins.region, force)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': token
                }

            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/infinstor/s3meta'\
                    + '?prefix=' + quote(prefix.lstrip('/')) \
                    + '&op=get-filestatus&bucket=' + bucket\
                    + '&gets3url=true'
            if 'time_spec' in self.timespec_info:
                time_spec = self.timespec_info['time_spec']
                if (len(time_spec) == 33): # infinslice
                    st, en = self.infinslice_to_epochs(time_spec)
                    url = url + '&startTime=' + str(st) + '&endTime=' + str(en)
                elif (len(time_spec) == 16): # infinsnap
                    url = url + '&endTime=' + str(self.infinsnap_to_epoch(time_spec))
            try:
                response = call_requests_get(url, headers=headers)
            except HTTPError as http_err:
                if http_err.response.status_code == 404: # not found
                    print(f"get_version_id({url}) returned error 404 {http_err}. Throwing botocore exception instead")
                    raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, caller_name)
                print('HTTP error occurred: ' + str(http_err))
                raise
            except Exception as err:
                print('Other error occurred: ' + str(err))
                raise
            if 'Login expired. Please login again' in response.text:
                continue
            js = response.json()
            if 'versionId' in js:
                return js['versionId'], js['s3url']
            else:
                print('get_version_id: versionId not present in response=' + json.dumps(js))
                return None, None
        print('get_version_id: Tried twice. Giving up')
        return None, None

    def get_presigned_url(self, bucket, prefix, run_id, method, continuation_param = None):
        """
        gets the presigned url from mlflow/artifacts/getpresignedurl() (for mlflow artifacts bucket) or mlflow/concurrent/getpresignedurl() (for user buckets) for the specified 'method'

        Args:
            bucket (str): bucket name
            prefix (str): prefix in the bucket
            run_id (str): _description_
            method (_type_): get_object, put_object, list_objects, list_objects_v2
            continuation_param (_type_, optional): _description_. Defaults to None.

        Returns:
            str: the presigned url
        """
        if run_id: # this block executes when concurrent is attempting to access an mlflow artifact s3 bucket (run_id exists).  Usually this is when one DAG node reads the output of a prior node
            headers = self.get_auth_header()
            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/artifacts/getpresignedurl'
            url = url + '?run_id=' + run_id
            url = url + '&path=' + quote(prefix)
            url = url + '&method=' + method
            if continuation_param:
                url = url + '&' + continuation_param
            response = call_requests_get(url, headers=headers, retry=False)
            respj = response.json()
            if 'presigned_url' in respj:
                presigned_url = respj['presigned_url']
            else:
                print('Error: failed to get presigned url', respj)
                raise
            return presigned_url
        else:  # this block executes when concurrent is attempting to access a non artifact s3 bucket (no run_id is involved).   Usually this is when a DAG node reads a an S3 bucket as input
            ## Use credentials for concurrent users
            headers = self.get_auth_header()
            url = 'https://' + builtins.concurrent_server + '/api/2.0/mlflow/concurrent/getpresignedurl'
            url = url + '?bucket=' + bucket
            url = url + '&path=' + quote(prefix)
            url = url + '&method=' + method
            if continuation_param:
                url = url + '&' + continuation_param
            response = call_requests_get(url, headers=headers)
            respj = response.json()
            if 'presigned_url' in respj:
                presigned_url = respj['presigned_url']
            else:
                print('Error: failed to get presigned url', respj)
            return presigned_url


    def list_objects_v2_presigned(self, request_bucket, request_prefix, run_id, **kwargs):
        continuation_param = None
        if ('Marker' in kwargs):
            continuation_param = 'Marker=' + kwargs['Marker']
        if ('ContinuationToken' in kwargs):
            continuation_param = 'ContinuationToken=' + quote(kwargs['ContinuationToken'])
        ps_url = self.get_presigned_url(request_bucket, request_prefix, run_id, 'list_objects_v2',
                                        continuation_param=continuation_param)
        response = call_requests_get(ps_url)
        respj = self.to_json_response(response, 'ListBucketResult')
        return respj

    def list_objects_presigned(self, request_bucket, request_prefix, run_id, **kwargs):
        continuation_param = None
        if ('Marker' in kwargs):
            continuation_param = 'Marker=' + quote(kwargs['Marker'])
        ps_url = self.get_presigned_url(request_bucket, request_prefix, run_id, 'list_objects',
                                        continuation_param=continuation_param)
        response = call_requests_get(ps_url)
        respj = self.to_json_response(response, 'ListBucketResult')
        return respj

    def list_objects_at(self, type2, *args, **kwargs):
        request_bucket = kwargs['Bucket']
        request_prefix = kwargs.get('Prefix')
        attempt = 0
        while attempt < 2:
            if attempt == 0:
                force = False
            else:
                force = True
            attempt = attempt + 1
            token = tokenfile.get_token(builtins.region, force)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': token
                }
            if type2:
                list_type = 2
            else:
                list_type = 1
            if not request_prefix:
                request_prefix = ''
            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/infinstor/s3meta'\
                    + '?prefix=' + quote(request_prefix.lstrip('/')) \
                    + '&op=list-objects&bucket=' + request_bucket + '&list-type=' + str(list_type)\
                    + '&output-format=json'
            if 'time_spec' in self.timespec_info:
                time_spec = self.timespec_info['time_spec']
                if (len(time_spec) == 33): # infinslice
                    st, en = self.infinslice_to_epochs(time_spec)
                    url = url + '&startTime=' + str(st) + '&endTime=' + str(en)
                elif (len(time_spec) == 16): # infinsnap
                    url = url + '&endTime=' + str(self.infinsnap_to_epoch(time_spec))
            if ('Delimiter' in kwargs):
                url = url + '&Delimiter=' + kwargs['Delimiter']
            if ('Marker' in kwargs):
                url = url + '&Marker=' + kwargs['Marker']
            if ('ContinuationToken' in kwargs):
                url = url + '&ContinuationToken=' + kwargs['ContinuationToken']
            if ('StartAfter' in kwargs):
                url = url + '&StartAfter=' + kwargs['StartAfter']
            if ('MaxKeys' in kwargs):
                url = url + '&MaxKeys=' + str(kwargs['MaxKeys'])
            try:
                response:requests.Response = call_requests_get(url, headers=headers)
                if not response.ok: _log_requests_Response(response)
                response.raise_for_status()
            except HTTPError as http_err:
                traceback.print_exc()
                if http_err.response.status_code == 404:
                    print('list_objects_at: got 404. No more objects', flush=True)
                    return {'Name': request_bucket, 'Contents': [], 'IsTruncated': False, 'Prefix': request_prefix}
                print('HTTP error occurred: ' + str(http_err))
                raise
            except Exception as err:
                traceback.print_exc()
                print('Other error occurred: ' + str(err))
                raise
            if 'Login expired. Please login again' in response.text:
                continue
            respj = response.json()
            if 'Contents' in respj:
                for one in respj['Contents']:
                    if 'LastModified' in one:
                        one['LastModified'] = datetime.fromtimestamp(one['LastModified']/1000)
            return respj
        print('list_objects_at: Tried twice. Giving up')
        return None

    def infinsnap_to_epoch(self, time_spec):
        if (len(time_spec) != 16 or not time_spec.startswith("tm")):
            raise ValueError('Incorrectly formatted infinsnap time_spec ' + time_spec)
        year = int(time_spec[2:6])
        month = int(time_spec[6:8])
        day = int(time_spec[8:10])
        hour = int(time_spec[10:12])
        minute = int(time_spec[12:14])
        second = int(time_spec[14:])
        dt = datetime(year, month, day, hour, minute, second, 0, tzinfo=timezone.utc)
        return int(dt.timestamp() * 1000.0)

    def infinslice_to_epochs(self, time_spec):
        if (len(time_spec) != 33 or not time_spec.startswith("tm")):
            raise ValueError('Incorrectly formatted infinslice time_spec ' + time_spec)
        year = int(time_spec[2:6])
        month = int(time_spec[6:8])
        day = int(time_spec[8:10])
        hour = int(time_spec[10:12])
        minute = int(time_spec[12:14])
        second = int(time_spec[14:16])
        dt1 = datetime(year, month, day, hour, minute, second, 0, tzinfo=timezone.utc)
        year = int(time_spec[19:23])
        month = int(time_spec[23:25])
        day = int(time_spec[25:27])
        hour = int(time_spec[27:29])
        minute = int(time_spec[29:31])
        second = int(time_spec[31:])
        dt2 = datetime(year, month, day, hour, minute, second, 0, tzinfo=timezone.utc)
        return int(dt1.timestamp() * 1000.0), int(dt2.timestamp() * 1000.0)

    def get_object(self, **kwargs):
        if self.timespec_info['type'] == 'infinsnap' or self.timespec_info['type'] == 'infinslice' or 'time_spec' in self.timespec_info:
            request_bucket = kwargs['Bucket']
            request_file = kwargs['Key']
            if request_bucket in self.timespec_info['infinsnap_buckets']: # infinsnap or infinslice
                versionId, ps_url = self.get_version_id(request_bucket, request_file, 'get_object')
                if (versionId != None):
                    if self.timespec_info['use_presigned_url_for_infinsnap']:
                        print(f"infin_boto3.get_object({request_bucket}, {request_file}). is infinsnap bucket. using ps_url", flush=True)
                        return self.get_object_presigned(request_bucket, ps_url)
                    else:
                        print(f"infin_boto3.get_object({request_bucket}, {request_file}). not configured with ps_url for infinsnap. sending to default", flush=True)
                        kwargs['VersionId'] = versionId
                        return self.defaultClient.get_object(**kwargs)
            elif request_bucket in self.timespec_info['concurrent_user_buckets']: # user bucket
                ps_url = self.get_presigned_url(request_bucket, request_file, None, 'get_object')
                print(f"infin_boto3.get_object({request_bucket}, {request_file}). is user bucket. using ps_url", flush=True)
                return self.get_object_presigned(request_bucket, ps_url)
            else: # mlflow artifact
                run_id = parse_run_id(request_file)
                if run_id:
                    ps_url = self.get_presigned_url(request_bucket, request_file, run_id, 'get_object')
                    print(f"infin_boto3.get_object({request_bucket}, {request_file}). is mlflow artifact. using ps_url", flush=True)
                    return self.get_object_presigned(request_bucket, ps_url)
                else:
                    print(f"infin_boto3.get_object({request_bucket}, {request_file}). not a mlflow artifact. sending to default", flush=True)
                    return self.defaultClient.get_object(**kwargs)
        else:
            print(f"infin_boto3.get_object({request_bucket}, {request_file}). no timespec. sending to default", flush=True)
            return self.defaultClient.get_object(**kwargs)

    def get_object_presigned(self, request_bucket, ps_url):
        parsed_url = urlparse(ps_url)
        if parsed_url.hostname in connection_pools:
            pool = connection_pools[parsed_url.hostname]
        else:
            pool = urllib3.HTTPSConnectionPool(parsed_url.hostname)
            connection_pools[parsed_url.hostname] = pool
        try:
            response = pool.request('GET', ps_url, preload_content=False, timeout=urllib3.Timeout(connect=5.0, read=10.0), retries=urllib3.Retry(3, redirect=2))
        except HTTPError as http_err:
            print(f"get_object_presigned::pool.request() threw {http_err}")
            traceback.print_exc()
            if http_err.response.status_code == 404: # not found
                print(f"pool.request returned error 404 {http_err}. Throwing botocore exception instead")
                raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, 'download_file')
        except Exception as ex:
            print(f"get_object_presigned::pool.request() threw ex={ex}")
            traceback.print_exc()
            raise
        if response.status == 404:
            _log_urllib3_Response(response)
            print(f"get_object_presigned: pool.request returned status 404. Throwing botocore exception instead")
            raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, 'get_object')
        elif response.status == 403:
            _log_urllib3_Response(response)
            raise Exception('Access Denied')
        clen = response.getheader('Content-Length')
        rv = {'Body': InfinStreamingBody(response, clen),
              'ContentLength': int(clen),
              'ContentType': response.getheader('Content-Type')}
        if response.getheader('Last-Modified'):
            rv['LastModified'] = datetime.strptime(
                response.getheader('Last-Modified'), '%a, %d %b %Y %H:%M:%S %Z')
        return rv

    def head_object(self, **kwargs):
        if self.timespec_info['type'] == 'infinsnap' or self.timespec_info['type'] == 'infinslice' or 'time_spec' in self.timespec_info:
            request_bucket = kwargs['Bucket']
            request_file = kwargs['Key']
            if request_bucket in self.timespec_info['infinsnap_buckets']: # infinsnap or infinslice
                versionId, ps_url = self.get_version_id(request_bucket, request_file, 'head_object')
                if (versionId != None):
                    if self.timespec_info['use_presigned_url_for_infinsnap']:
                        print(f"infin_boto3.head_object({request_bucket}, {request_file}). is infinsnap bucket. using ps_url", flush=True)
                        return self.head_object_presigned(request_bucket, ps_url)
                    else:
                        print(f"infin_boto3.head_object({request_bucket}, {request_file}). not configured with ps_url for infinsnap. sending to default", flush=True)
                        kwargs['VersionId'] = versionId
                        return self.defaultClient.head_object(**kwargs)
            elif request_bucket in self.timespec_info['concurrent_user_buckets']: # user bucket
                ps_url = self.get_presigned_url(request_bucket, request_file, None, 'head_object')
                print(f"infin_boto3.head_object({request_bucket}, {request_file}). is user bucket. using ps_url", flush=True)
                return self.head_object_presigned(request_bucket, ps_url)
            else: # mlflow artifact
                run_id = parse_run_id(request_file)
                if run_id:
                    ps_url = self.get_presigned_url(request_bucket, request_file, run_id, 'head_object')
                    print(f"infin_boto3.head_object({request_bucket}, {request_file}). is mlflow artifact. using ps_url", flush=True)
                    return self.head_object_presigned(request_bucket, ps_url)
                else:
                    print(f"infin_boto3.head_object({request_bucket}, {request_file}). not a mlflow artifact. sending to default", flush=True)
                    return self.defaultClient.head_object(**kwargs)
        else:
            print(f"infin_boto3.head_object({request_bucket}, {request_file}). no timespec. sending to default", flush=True)
            return self.defaultClient.head_object(**kwargs)

    def head_object_presigned(self, request_bucket, ps_url):
        parsed_url = urlparse(ps_url)
        if parsed_url.hostname in connection_pools:
            print(f'head_object_presigned: hostname={parsed_url.hostname} is in pool cache')
            pool = connection_pools[parsed_url.hostname]
        else:
            print(f'head_object_presigned: hostname={parsed_url.hostname} is NOT in pool cache')
            pool = urllib3.HTTPSConnectionPool(parsed_url.hostname)
            connection_pools[parsed_url.hostname] = pool
        try:
            response:urllib3.response.HTTPResponse = pool.request('GET', ps_url, preload_content=False, timeout=urllib3.Timeout(connect=5.0, read=10.0), retries=urllib3.Retry(3, redirect=2))
        except HTTPError as http_err:
            print(f"pool.request threw http_err={http_err}")
            traceback.print_exc()
            if http_err.response.status_code == 404: # not found
                print(f"pool.request returned error 404 {http_err}. Throwing botocore exception instead")
                raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, 'download_file')
        except Exception as ex:
            print(f"pool.request threw ex={ex}")
            traceback.print_exc()
            raise
        if response.status == 404:
            print(f"head_object_presigned: pool.request returned status 404. Throwing botocore exception instead")
            _log_urllib3_Response(response)
            raise ClientError({'Error': {'Code': '404', 'Message': 'Not Found'}}, 'head_object')
        elif response.status == 403:
            _log_urllib3_Response(response)
            raise Exception('Access Denied')
        clen = response.getheader('Content-Length')
        rv = {'ContentLength': int(clen),
              'ContentType': response.getheader('Content-Type')}
        if response.getheader('Last-Modified'):
            rv['LastModified'] = datetime.strptime(
                response.getheader('Last-Modified'), '%a, %d %b %Y %H:%M:%S %Z')
        return rv

    def get_paginator(self, operation_name):
        print('get_paginator', operation_name)
        if operation_name == 'list_objects':
            self.print_greeting("get_paginator:list_objects")
            return ListObjectsPaginator(False, self, self.timespec_info['infinsnap_buckets'],
                                        self.timespec_info['non_infinsnap_buckets'],
                                        self.timespec_info.get('concurrent_user_buckets', []))
        elif operation_name == 'list_objects_v2':
            self.print_greeting("get_paginator:list_objects_v2")
            return ListObjectsPaginator(True, self, self.timespec_info['infinsnap_buckets'],
                                        self.timespec_info['non_infinsnap_buckets'],
                                        self.timespec_info.get('concurrent_user_buckets', []))
        else:
            print("get_paginator: Fall back to default client")
            return self.defaultClient.get_paginator(operation_name)

    def get_putobject_presigned_url(self, bucket, prefix, **kwargs):
        attempt = 0
        while attempt < 2:
            if attempt == 0:
                force = False
            else:
                print('get_putobject_presigned_url: attempt = ' + str(attempt) + ', force True')
                force = True
            attempt = attempt + 1
            token = tokenfile.get_token(builtins.region, force)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': token
                }

            url = 'https://' + builtins.mlflowserver + '/api/2.0/mlflow/infinstor/s3meta'\
                    + '?prefix=' + quote(prefix.lstrip('/')) \
                    + '&op=get-putobject-presigned-url&bucket=' + bucket
            if kwargs:
                if 'ExtraArgs' in kwargs:
                    if 'Metadata' in kwargs['ExtraArgs']:
                        url = url + "&metadata=" + quote(json.dumps(kwargs['ExtraArgs']['Metadata']))
            try:
                response:requests.Response = call_requests_get(url, headers=headers)
                if not response.ok: _log_requests_Response(response)
            except HTTPError as http_err:
                traceback.print_exc()
                print('HTTP error occurred: ' + str(http_err))
                raise
            except Exception as err:
                traceback.print_exc()
                print('Other error occurred: ' + str(err))
                raise
            if 'Login expired. Please login again' in response.text:
                continue
            js = response.json()
            if 's3url' in js:
                return js['s3url']
            else:
                print('get_putobject_presigned_url: s3url not present in response=' + json.dumps(js))
                return None
        print('get_putobject_presigned_url: Tried twice. Giving up')
        return None
    
    def _get_http_headers_for_sig_version_s3v4(self, kwargs:dict) -> dict:
        http_headers:dict = {}
        
        # response = s3client.upload_file(fn, args.bucket, obj_name, ExtraArgs={"Metadata": {"infinsnap_start": str(start_time_epochms), "infinsnap_end": str(end_time_epochms)}})
        # 
        # if object metadata is specified, convert them to http headers.  This is needed for newer boto3 s3 signature_version='s3v4' argument in boto3.client('s3') call.  
        # For the default signature_version in boto3.client('s3') call, setting these headers is not needed
        #
        # check if the 'Metadata' is set for the object
        if kwargs.get('ExtraArgs') and kwargs.get('ExtraArgs').get('Metadata'):
            metadata:dict = kwargs.get('ExtraArgs').get('Metadata')
            for key in metadata.keys():
                # create the header for the 'key'
                http_headers['x-amz-meta-' + key] = metadata[key]
        
        return http_headers

    def upload_file(self, *args, **kwargs):
        request_file = args[0]
        request_bucket = args[1]
        request_object = args[2]
        print(f"upload_file: file {request_file}, bucket {request_bucket}, obj {request_object}. kwargs={kwargs}")
        if self.timespec_info['use_presigned_url_for_infinsnap'] \
                and request_bucket in self.timespec_info['infinsnap_buckets'] \
                or request_bucket in self.timespec_info['non_infinsnap_buckets']:
            self.print_greeting("upload_file")
            ps_url = self.get_putobject_presigned_url(request_bucket, request_object, **kwargs)
            if ps_url:
                with open(request_file, 'rb') as fp:
                    file_data = fp.read()
                    # response = s3client.upload_file(fn, args.bucket, obj_name, ExtraArgs={"Metadata": {"infinsnap_start": str(start_time_epochms), "infinsnap_end": str(end_time_epochms)}})
                    # 
                    # if object metadata is specified, convert them to http headers.  This is needed for newer boto3 s3 signature_version='s3v4'.  
                    # For the default signature_version, setting these headers is not needed
                    headers:dict = self._get_http_headers_for_sig_version_s3v4(kwargs)
                    
                    hr:requests.Response = requests.put(ps_url, data=file_data, headers=headers, timeout=7200)
                    if hr.status_code != 200:
                        print(f'infin_boto3: Warning. upload_file response for ps_url={ps_url} was '
                            + str(hr.status_code) + '. Expected 200')
                        _log_requests_Response(hr)
                    else:
                        print(f'infin_boto3: upload_file response was 200 for {ps_url}')
            else:
                print('infin_boto3: Unable to get presigned URL. Upload failed')
        else:
            print(f"upload_file: file {request_file}, bucket {request_bucket}, obj {request_object}. kwargs={kwargs}. BYPASS")
            return self.defaultClient.upload_file(*args, **kwargs)

    def __getattr__(self, attr):
        if attr == 'list_objects':
            return self.list_objects
        elif attr == 'list_objects_v2':
            return self.list_objects_v2
        elif attr == 'download_file':
            return self.download_file
        elif attr == 'get_object':
            return self.get_object
        elif attr == 'head_object':
            return self.head_object
        elif attr == 'get_paginator':
            return self.get_paginator
        elif attr == 'upload_file':
            return self.upload_file
        else:
            return getattr(self.defaultClient, attr)

# returns bucketlist, use_presigned_url_for_infinsnap
def get_customerinfo() -> Tuple[List[str], bool, bool]:
    """
    _summary_

    _extended_summary_

    Returns:
        Tuple[List[str], bool, bool]: list of buckets, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow
    """
    
    # if running in concurrent environment and not in an infinstorMlflow environment, /customerinfo API doesn't apply.  So stub it
    if ( builtins.isConcurrent and not builtins.isInfinMlflowServer ):
        return ([], True, True)
    
    # at this point, we are running in an infinstor mlflow environment, so get /customerinfo REST API
    token = tokenfile.get_token(builtins.region, False)
    global user_info_cache
    if 'customer_info' in user_info_cache:
        if user_info_cache['customer_info'][3] == token:
            return user_info_cache['customer_info'][0], user_info_cache['customer_info'][1], user_info_cache['customer_info'][2]
        else:
            print("found customer info in cache, but token has changed. resetting customerinfo ...")
    else:
        print("no customer info in cache")

    payload = "ProductCode=9fcazc4rbiwp6ewg4xlt5c8fu"
    headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': token
            }

    url = 'https://' + builtins.apiserver + '/customerinfo'

    num_attempts = 3
    while num_attempts > 0:
        num_attempts -= 1
        try:
            response = requests.post(url, data=payload+'&clientType=browser', headers=headers)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}, Try {num_attempts} more times')
            time.sleep(60)
            continue
        except Exception as err:
            print(f'Other error occurred: {err}, Try {num_attempts} more times')
            time.sleep(60)
            continue
        else:
            rv = []
            rj = response.json()
            if 'InfinSnapBuckets' in rj:
                for onebucket in rj['InfinSnapBuckets']:
                    rv.append(onebucket)
            if 'usePresignedUrlForInfinSnap' in rj and rj['usePresignedUrlForInfinSnap'] == 'true':
                print('get_customerinfo: usePresignedUrlForInfinSnap='
                        + str(rj['usePresignedUrlForInfinSnap']))
                use_presigned_url_for_infinsnap = True
            else:
                print('get_customerinfo: no usePresignedUrlForInfinSnap')
                use_presigned_url_for_infinsnap = False

            if 'usePresignedUrlForMLflow' in rj and rj['usePresignedUrlForMLflow'] == 'true':
                print('get_customerinfo: usePresignedUrlForMLflow='
                      + str(rj['usePresignedUrlForMLflow']))
                use_presigned_url_for_mlflow = True
            else:
                print('get_customerinfo: no usePresignedUrlForMLflow')
                use_presigned_url_for_mlflow = False

            user_info_cache['customer_info'] = rv, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow, token
            return rv, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow

##Decorators are specific to functions

def is_infinsnap_bucket(onebucket):
    if 'ddbTable' in onebucket and onebucket['ddbTable'] is not None:
        return True
    else:
        return False


def fetch_concurrent_user_buckets():
    global user_info_cache

    if 'user_buckets' in user_info_cache:
        return user_info_cache['user_buckets']

    concurrent_user_buckets = []
    if 'MLFLOW_CONCURRENT_URI' in os.environ:
        url = os.environ['MLFLOW_CONCURRENT_URI'].rstrip('/') + '/api/2.0/mlflow/concurrent/getuserbuckets'
        token = tokenfile.get_token(builtins.region, False)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': token
        }

        try:
            response = call_requests_get(url, headers=headers)
        except HTTPError as http_err:
            print('HTTP error occurred: ' + str(http_err))
            raise
        except Exception as err:
            print('Other error occurred: ' + str(err))
            raise
        js = response.json()
        concurrent_user_buckets = js.get('buckets', [])

    user_info_cache['user_buckets'] = concurrent_user_buckets
    print('User Buckets: ', concurrent_user_buckets)
    return concurrent_user_buckets



##Decorator for boto3.Session.client
def decorate_boto3_client(client_func):
    orig_func = client_func
    @functools.wraps(client_func)
    def wrapper(*args, **kwargs):
        active_run = mlflow.active_run()
        if not active_run and 'MLFLOW_RUN_ID' in os.environ:
            active_run = mlflow.tracking.MlflowClient().get_run(os.environ['MLFLOW_RUN_ID'])
        if args[1] == 's3':
            concurrent_user_buckets = fetch_concurrent_user_buckets()
            if 'infinstor_time_spec' in kwargs:
                time_spec = kwargs['infinstor_time_spec']
                del kwargs['infinstor_time_spec']
                print('infinstor: Activating time_spec=' + time_spec)
                bucket_infos, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow = get_customerinfo()
                if (len(time_spec) == 33):
                    timespec_info = {
                        'type': 'infinslice',
                        'time_spec': time_spec,
                        'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                              is_infinsnap_bucket(onebucket)],
                        'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                                  not is_infinsnap_bucket(onebucket)],
                        'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                        'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                        'concurrent_user_buckets': concurrent_user_buckets
                    }
                elif (len(time_spec) == 16):
                    timespec_info = {
                        'type': 'infinsnap',
                        'time_spec': time_spec,
                        'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                              is_infinsnap_bucket(onebucket)],
                        'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                                  not is_infinsnap_bucket(onebucket)],
                        'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                        'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                        'concurrent_user_buckets': concurrent_user_buckets
                    }
                else:
                    raise ValueError('Incorrectly formatted infinstor_time_spec '
                            + str(time_spec))
                defaultClient = orig_func(*args, **kwargs)
                return InfinBotoClient(defaultClient, timespec_info)
            elif builtins.mlflowserver and active_run != None:
                if ('INFINSTOR_SNAPSHOT_TIME' in os.environ):
                    epoch_time = get_epoch_time_from_env(os.environ['INFINSTOR_SNAPSHOT_TIME'])
                else:
                    epoch_time = active_run.info.start_time
                mlflow.tracking.MlflowClient().log_param(active_run.info.run_id, 'infinstor_snapshot_time', epoch_time)
                time_spec = infinstor.infinsnap(datetime.fromtimestamp(epoch_time/1000))
                bucket_infos, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow = get_customerinfo()
                timespec_info = {
                        'type': 'infinsnap',
                        'epoch_time': epoch_time,
                        'time_spec': time_spec,
                        'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                        'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                               is_infinsnap_bucket(onebucket)],
                        'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                                  not is_infinsnap_bucket(onebucket)],
                        'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                        'concurrent_user_buckets': concurrent_user_buckets
                }
                print('infinstor: Activating implicit infinsnap/slice. Snapshot time='
                    + datetime.fromtimestamp(epoch_time/1000).strftime("%m/%d/%Y %H:%M:%S"))
                defaultClient = orig_func(*args, **kwargs)
                return InfinBotoClient(defaultClient, timespec_info)
            else:
                bucket_infos, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow = get_customerinfo()
                timespec_info = {
                    'type': 'infinsnap',
                    'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                    'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                          is_infinsnap_bucket(onebucket)],
                    'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                              not is_infinsnap_bucket(onebucket)],
                    'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                    'concurrent_user_buckets': concurrent_user_buckets
                }
                defaultClient = orig_func(*args, **kwargs)
                return InfinBotoClient(defaultClient, timespec_info)
        defaultClient = orig_func(*args, **kwargs)
        return defaultClient
    return wrapper

def get_epoch_time_from_env(envvar):
    if envvar.startswith('run:/'):
        client = MlflowClient()
        run = client.get_run(envvar[5:])
        for key, value in run.data.params.items():
            if key == 'infinstor_snapshot_time':
                return int(value)
        # No infinstor_snapshot_time param. use run start time
        return run.info.start_time
    else:
        return int(envvar)


def call_requests_get(url, headers=None, retry=False) -> requests.Response :
    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    try:
        if headers:
            response = session.get(url, headers=headers, timeout=7200)
        else:
            response = session.get(url, timeout=7200)
        if not response.ok: _log_requests_Response(response)
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        raise
    except Exception as ex:
        print(f'Exception {ex} in request ' + str(ex) + ", for url: " + url)
        raise ex


##Decorator for boto3.Session.resource
def decorate_boto3_resource(resource_func):
    orig_func = resource_func
    @functools.wraps(resource_func)
    def wrapper(*args, **kwargs):
        active_run = mlflow.active_run()
        if not active_run and 'MLFLOW_RUN_ID' in os.environ:
            active_run = mlflow.tracking.MlflowClient().get_run(os.environ['MLFLOW_RUN_ID'])
        concurrent_user_buckets = fetch_concurrent_user_buckets()
        if 'infinstor_time_spec' in kwargs:
            time_spec = kwargs['infinstor_time_spec']
            del kwargs['infinstor_time_spec']
            print('infinstor: Activating time_spec=' + time_spec)
            bucket_infos, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow = get_customerinfo()
            if bucket_infos:
                if (len(time_spec) == 33):
                    timespec_info = {
                        'type': 'infinslice',
                        'time_spec': time_spec,
                        'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                        'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                              is_infinsnap_bucket(onebucket)],
                        'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                                  not is_infinsnap_bucket(onebucket)],
                        'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                        'concurrent_user_buckets': concurrent_user_buckets
                        }
                elif (len(time_spec) == 16):
                    timespec_info = {
                        'type': 'infinsnap',
                        'time_spec': time_spec,
                        'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                        'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                              is_infinsnap_bucket(onebucket)],
                        'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                                  not is_infinsnap_bucket(onebucket)],
                        'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                        'concurrent_user_buckets': concurrent_user_buckets
                        }
                else:
                    raise ValueError('Incorrectly formatted infinstor_time_spec '
                        + str(time_spec))
                defaultResource = orig_func(*args, **kwargs)
                return InfinBotoResource(defaultResource, timespec_info)
            elif builtins.mlflowserver and active_run != None:
                if ('INFINSTOR_SNAPSHOT_TIME' in os.environ):
                    epoch_time = get_epoch_time_from_env(os.environ['INFINSTOR_SNAPSHOT_TIME'])
                else:
                    epoch_time = active_run.info.start_time
                time_spec = infinstor.infinsnap(epoch_time)
                mlflow.tracking.MlflowClient().log_param(active_run.info.run_id, 'infinstor_snapshot_time', epoch_time)
                bucket_infos, use_presigned_url_for_infinsnap, use_presigned_url_for_mlflow = get_customerinfo()
                timespec_info = {
                        'type':'infinsnap',
                        'epoch_time': epoch_time,
                        'time_spec': time_spec,
                        'use_presigned_url_for_infinsnap': use_presigned_url_for_infinsnap,
                        'infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                              is_infinsnap_bucket(onebucket)],
                        'non_infinsnap_buckets': [onebucket['bucketname'] for onebucket in bucket_infos if
                                                  not is_infinsnap_bucket(onebucket)],
                        'use_presigned_url_for_mlflow': use_presigned_url_for_mlflow,
                        'concurrent_user_buckets': concurrent_user_buckets
                    }
                print('infinstor: Activating implicit infinsnap/slice. Snapshot time='
                    + datetime.fromtimestamp(epoch_time/1000).strftime("%m/%d/%Y %H:%M:%S"))
                defaultResource = orig_func(*args, **kwargs)
                return InfinBotoResource(defaultResource, timespec_info)
        defaultResource = orig_func(*args, **kwargs)
        return defaultResource
    return wrapper

def get_infin_output_location(run_id=None, default_bucket=None, default_prefix="/"):
    if not run_id:
        active_run = mlflow.active_run()
        if active_run:
            run_id = mlflow.active_run().info.run_id
        elif 'MLFLOW_RUN_ID' in os.environ:
            run_id = os.environ['MLFLOW_RUN_ID']
    if run_id:
        client = mlflow.tracking.MlflowClient()
        run = client.get_run(run_id)
        artifact_uri = run.info.artifact_uri
        parse_result = urlparse(artifact_uri)
        if (parse_result.scheme != 's3'):
            raise ValueError('Error. Do not know how to deal with artifacts in scheme ' \
                             + parse_result.scheme)
        bucketname = parse_result.netloc
        prefix = parse_result.path.lstrip('/')
        return bucketname, prefix
    else:
        return default_bucket, default_prefix

get_version_resp:bootstrap.GetVersionResponse = bootstrap.bootstrap_config_values_from_mlflow_rest_if_needed()
boto3.Session.client = decorate_boto3_client(boto3.Session.client)
boto3.Session.resource = decorate_boto3_resource(boto3.Session.resource)

###Intercepting Logic####
"""
1. User declares an input bucket
2. If input spec is infinsnap or infinslice
    If bucket in inputspec is same as declared input bucket
        change the endpoint url
        don't intercept any other calls --> THIS WILL CHANGE FOR PARTITIONING
    else
        don't change anything
3. If the input spec is mlflow artifact
    Don't change the endpoint url, but intercept the read/list
    if bucket in the call is same as declared input bucket
        change the bucket to the mlflow artifact uri bucket
    else
        don't do anything
"""

