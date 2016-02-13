#!/usr/bin/env python3
import os
import sys
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban

from celery import group
from tqdm import tqdm
from tasks import movie_base_task, movie_full_task, down_images_task, get_douban_task_group

from celery.signals import task_success


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
    if sys.argv[1] == 'main':
        print('Preparing, please wait, about 1 min...(no progress bar)')
        douban_ids = movie_base_task.delay(10).get()
        print('Preparation Completed.')
        
        g = get_douban_task_group(douban_ids, movie_full_task)

        async_result = g.apply_async()
        
        print('Start get movie full data:')
        print_progress(async_result, 'get movie full data')


    elif sys.argv[1] == 'image':
        print('Start down movie images(about use 10+h, 40G):')
        print_progress(async_result, "down movie images")
        from webs.douban.tasks.get_main_movies_base_data import movie_douban_ids as douban_ids

        douban_ids = list(douban_ids)
        g = get_douban_task_group(douban_ids, down_images_task, group_size=5)

        async_result = g.apply_async()

