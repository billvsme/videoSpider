#!/usr/bin/env python3
import os
import time
import sys
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban

from celery import group
from tasks import movie_base_task, movie_full_task, down_images_task


if __name__ == '__main__':
    start = time.time()

    if sys.argv[1] == 'celery':
        douban_ids = movie_base_task.delay().get()

        
        start = time.time()

        movie_size = len(douban_ids)
        process_number = 20

        movie_full_subtasks = [
            movie_full_task.s(
                douban_ids[x : x+process_number],
                process_number
            ) for x in range(0, movie_size, process_number)
        ]

        g = group(movie_full_subtasks)

        t = g.apply_async()


        completed_count = 0
        while(completed_count != len(movie_full_subtasks)):
            completed_count = t.completed_count()
            print(completed_count/len(movie_full_subtasks))

        end = time.time()

        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'image':
        douban_ids = movie_base_task.delay().get()
        start = time.time()
        movie_size = len(douban_ids)

        process_number = 5

        movie_full_subtasks = [
            down_images_task.s(
                douban_ids[x : x+process_number],
                process_number
            ) for x in range(0, movie_size, process_number)
        ]

        g = group(movie_full_subtasks)

        t = g.apply_async()


        completed_count = 0
        while(completed_count != len(movie_full_subtasks)):
            completed_count = t.completed_count()
            print(completed_count/len(movie_full_subtasks))

        end = time.time()

        print('use {}s'.format(end-start))
        '''

        from webs import douban
        douban.tasks.down_images.create_requests_and_save_datas('5501681')

        '''
