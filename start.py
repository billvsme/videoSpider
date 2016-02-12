#!/usr/bin/env python3
import os
import time
import sys
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban

from celery import group
from tasks import movie_base_task, movie_full_task, down_images_task, get_douban_task_group


def print_progress(async_result):
    completed_count = 0
    while(completed_count != len(async_result)):
        completed_count = async_result.completed_count()
        print(completed_count/len(async_result))


if __name__ == '__main__':
    start = time.time()

    if sys.argv[1] == 'celery':
        douban_ids = movie_base_task.delay().get()
        
        start = time.time()
        g = get_douban_task_group(douban_ids, movie_full_task)

        async_result = g.apply_async()
        
        print_progress(async_result)

        end = time.time()

        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'image':
        from webs.douban.tasks.get_main_movies_base_data import movie_douban_ids as douban_ids

        douban_ids = list(douban_ids)
        start = time.time()
        g = get_douban_task_group(douban_ids, down_images_task, group_size=5)

        async_result = g.apply_async()

        print_progress(async_result)

        end = time.time()

        print('use {}s'.format(end-start))
        '''

        from webs import douban
        douban.tasks.down_images.create_requests_and_save_datas('5501681')

        '''
