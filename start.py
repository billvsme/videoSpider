#!/usr/bin/env python3
import os
import sys
import models
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban
from config import sqla; session = sqla['session']

from celery import group
from tqdm import tqdm
from tasks import (movie_base_task,
                   movie_full_task,
                   celebry_full_task,
                   down_images_task,
                   get_douban_task_group)

from celery.signals import task_success

#from webs.douban.tasks.get_main_movies_base_data import movie_douban_ids as douban_ids

def print_progress(async_result, desc):
    pbar = tqdm(total=len(async_result), desc=desc)
    completed_count = 0
    while(completed_count != len(async_result)):
        update_completed_count = async_result.completed_count()
        updata_count = update_completed_count - completed_count
        if updata_count != 0:
            pbar.update(updata_count)
        completed_count = update_completed_count


if __name__ == '__main__':
    if sys.argv[1] == 'movie':
        print('Preparing, please wait, about 1 min...(no progress bar)')
        douban_ids = movie_base_task.delay(10).get()
        print('Preparation Completed.')
        
        g = get_douban_task_group(douban_ids, movie_full_task)

        print('Start get movie full data:')
        async_result = g.apply_async()
        print_progress(async_result, 'get movie full data')

        

    if sys.argv[1] == 'celebry':
        print('Start get celebry data:')

        douban_ids = []
        for douban_id, in session.query(models.Celebrity.douban_id):
            douban_ids.append(douban_id)

        g = get_douban_task_group(douban_ids, celebry_full_task)
        async_result = g.apply_async()
        print_progress(async_result, 'get celery data')


    elif sys.argv[1] == 'image':
        print('Start down movie images(about use 10+h, 40G):')

        douban_ids = []
        for douban_id, in session.query(models.Movie.douban_id):
            douban_ids.add(douban_id)

        douban_ids = list(douban_ids)
        g = get_douban_task_group(douban_ids, down_images_task, group_size=5)

        async_result = g.apply_async()
        print_progress(async_result, "down movie images")

