# -*- coding: utf-8 -*-
import os
import qiniu
from qiniu import Auth
from gevent import monkey
from gevent.pool import Pool

from config import config

monkey.patch_socket()


def down(token, key, localfile, mime_type, delete=False):
    ret, info = qiniu.put_file(
                    token, key, localfile,
                    mime_type=mime_type,
                    check_crc=True
                )
    assert ret['key'] == key
    assert ret['hash'] == qiniu.etag(localfile)

    print(localfile)
    if delete:
        os.remove(localfile)


def upload_qiniu_by_path(access_key, secret_key, bucket_name, key_prefix,
                         pool_number, path, delete=False):
    q = Auth(access_key, secret_key)
    mime_type = "text/plain"
    params = {'x:a': 'a'}

    pool = Pool(pool_number)

    for dirpath, dirnames, filenames in os.walk(path):
        print(dirpath)
        if len(filenames) > 0:
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                localfile = os.path.join(dirpath, filename)
                key = os.path.join(key_prefix, localfile.replace(path, '')[1:])
                token = q.upload_token(bucket_name, key)

                pool.spawn(
                    down,
                    token=token,
                    key=key,
                    localfile=localfile,
                    mime_type=mime_type,
                    delete=delete
                )


def upload_qiniu_by_filenames(access_key, secret_key, bucket_name, key_prefix,
                              pool_number, path, filenames, delete=False):
    q = Auth(access_key, secret_key)
    mime_type = "text/plain"
    params = {'x:a': 'a'}

    pool = Pool(pool_number)

    for filename in filenames:
        localfile = filename
        key = os.path.join(key_prefix, localfile.replace(path, '')[1:])
        token = q.upload_token(bucket_name, key)

        pool.spawn(
            down,
            token=token,
            key=key,
            localfile=localfile,
            mime_type=mime_type,
            delete=delete
        )

    pool.join()

'''

access_key = config.get('qiniu', 'access_key')
secret_key = config.get('qiniu', 'secret_key')
bucket_name = config.get('qiniu', 'bucket_name')

path = '/Users/billvsme/work/videoSpider/photo6'

upload_qiniu(access_key, secret_key, bucket_name, '/static/img/' ,100, path)
'''
