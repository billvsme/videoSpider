#!/usr/bin/env python3
import os
import time
import sys
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban

from celery import group
from tasks import movie_base_task, movie_full_task


if __name__ == '__main__':
    start = time.time()

    '''
    if len(sys.argv)  == 1:
        os.system('python start.py full')
    elif sys.argv[1] == 'base':
        douban.tasks.get_main_movies_base_data.start_work()

        end = time.time()
        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'movie':
        douban.tasks.get_main_movies_full_data.start_work(process_number=2)

        end = time.time()
        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'celebrity':
        douban.tasks.get_celebrities_full_data.start_work(process_number=2)

    elif sys.argv[1] == 'full':
        os.system('python start.py base')
        os.system('python start.py movie')
        os.system('python start.py celebrity')
        end = time.time()
        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'test':
        douban.tasks.get_main_movies_full_data.start_work()
        douban.tasks.get_celebrities_full_data.start_work()
        end = time.time()
        print('use {}s'.format(end-start))

    '''
    if sys.argv[1] == 'celery':
        douban_ids = movie_base_task.delay().get()

        
        start = time.time()

        movie_size = len(douban_ids)
        process_number = 20
        print('=============')
        print(movie_size)

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
