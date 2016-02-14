import sys
from celery import Celery, group
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
def celebry_full_task(douban_ids, pool_number):
    try:
        douban.tasks.get_celebrities_full_data.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        celebry_full_task.retry(countdown=10)

@app.task
def down_images_task(douban_ids, pool_number):
    try:
        douban.tasks.down_images.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        down_images_task.retry(countdown=10)


def get_douban_task_group(douban_ids, douban_task, group_size=20):
    douban_size = len(douban_ids)
    douban_subtasks = [
        douban_task.s(
            douban_ids[x: x+group_size],
            group_size
        ) for x in range(0, douban_size, group_size)
    ]

    g = group(douban_subtasks)

    return g
