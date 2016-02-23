import sys
from whoosh.index import create_in
from whoosh.fields import *
from celery import Celery, group
from config import sqla, ix
from whoosh.writing import AsyncWriter
from webs import douban
from gevent import monkey
monkey.patch_socket()

app = Celery('tasks', backend='db+sqlite:///celery_backend.sqlite', broker='sqla+sqlite:///celery_borker.sqlite')

@app.task
def movie_base_task(pool_number):
    movie_douban_ids = douban.tasks.get_main_movies_base_data.task(pool_number)
    return movie_douban_ids

@app.task
def movie_full_task(douban_ids, pool_number):
    try:
        douban.tasks.get_main_movies_full_data.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        movie_full_task.retry(countdown=10)

@app.task
def celebrity_full_task(douban_ids, pool_number):
    try:
        douban.tasks.get_celebrities_full_data.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        celebrity_full_task.retry(countdown=10)

@app.task
def down_video_images_task(douban_ids, pool_number):
    try:
        douban.tasks.down_video_images.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        down_images_task.retry(countdown=10)

@app.task
def down_celebrity_images_task(douban_ids, pool_number):
    try:
        douban.tasks.down_celebrity_images.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        down_images_task.retry(countdown=10)

@app.task
def upload_images_task(filenames, pool_number):
    from helpers import upload_qiniu_by_filenames
    from config import config
    access_key = config.get('qiniu', 'access_key')
    secret_key = config.get('qiniu', 'secret_key')
    bucket_name = config.get('qiniu', 'bucket_name')
    try:
        upload_qiniu_by_filenames(
            access_key,
            secret_key,
            bucket_name,
            '/static/img/',
            10, 
            config.get('photo', 'path'),
            filenames,
            True
        )
    except:
        print('Error ***************************')
        upload_images_task.retry(countdown=10)
    

@app.task
def whoosh_task(ids, pool_number, model_class):
    session = sqla['session']

    writer =  AsyncWriter(ix)
    for id_ in ids:
        obj = session.query(model_class).filter_by(id=id_).one()
        if obj.title is None or obj.summary is None:
            continue

        writer.add_document(
            title=obj.title,
            summary=obj.summary
        )
        print(obj.id)

    writer.commit()


def get_douban_task_group(douban_ids, douban_task, **kwargs):
    douban_size = len(douban_ids)
    if 'group_size' in kwargs:
        group_size = kwargs.pop('group_size')
    else:
        group_size = 20
    kwargs['pool_number'] = group_size
    douban_subtasks = [
        douban_task.s(
            douban_ids[x: x+group_size],
            **kwargs
        ) for x in range(0, douban_size, group_size)
    ]

    g = group(douban_subtasks)

    return g
