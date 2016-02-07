import sys
from celery import Celery
from webs import douban
from gevent import monkey;
monkey.patch_socket()


app = Celery('tasks', backend='db+sqlite:///celery_backend.sqlite', broker='sqla+sqlite:///celery_borker.sqlite')

@app.task
def movie_base_task():
    movie_douban_ids = douban.tasks.get_main_movies_base_data.task()
    return movie_douban_ids

@app.task
def movie_full_task(douban_ids, pool_number):
    try:
        douban.tasks.get_main_movies_full_data.task(douban_ids, pool_number)
    except:
        print('Error ***************************')
        self.retry(countdown=10)
