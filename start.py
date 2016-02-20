#!/usr/bin/env python3
import os
import sys
import models
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban
from config import config
from config import sqla; session = sqla['session']

from celery import group
from tqdm import tqdm
from tasks import (movie_base_task,
                   movie_full_task,
                   celebrity_full_task,
                   down_video_images_task,
                   down_celebrity_images_task,
                   upload_images_task,
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
    if sys.argv[1] == 'video':
        print('Preparing, please wait, about 1 min...(no progress bar)')
        douban_ids = movie_base_task.delay(20).get()
        print('Preparation Completed.')
        
        g = get_douban_task_group(douban_ids, movie_full_task)

        print('Start get movie full data:')
        async_result = g.apply_async()
        print_progress(async_result, 'get movie full data')

        

    if sys.argv[1] == 'celebrity':
        print('Start get celebrity data:')

        douban_ids = []
        for douban_id, in session.query(models.Celebrity.douban_id):
            douban_ids.append(douban_id)

        g = get_douban_task_group(douban_ids, celebrity_full_task)
        async_result = g.apply_async()
        print_progress(async_result, 'get celery data')

    if sys.argv[1] == 'full':
        os.system('python start.py video') 
        os.system('python start.py celebrity') 


    elif sys.argv[1] == 'down-image':
        print('Start down movie images(about use 10+h, 40G):')

        douban_ids = []
        for douban_id, in session.query(models.Movie.douban_id):
            douban_ids.append(douban_id)

        douban_ids = list(douban_ids)
        g = get_douban_task_group(douban_ids, down_video_images_task, group_size=5)

        async_result = g.apply_async()
        print_progress(async_result, "down video images")


        douban_ids = []
        for douban_id, in session.query(models.Celebrity.douban_id):
            douban_ids.append(douban_id)

        douban_ids = list(douban_ids)
        g = get_douban_task_group(douban_ids, down_celebrity_images_task, group_size=5)

        async_result = g.apply_async()
        print_progress(async_result, "down celebrity images")

    elif sys.argv[1] == 'upload-image':
        print('Preparing, please wait, about 1 min...(no progress bar)')
        photo_filenames = []
        for dirpath, dirnames, filenames in os.walk(config.get('photo', 'path')):
            print(dirpath)
            if len(filenames) > 0:
                for filename in filenames:
                    if filename.startswith('.'):
                        continue
                    
                    localfile = os.path.join(dirpath, filename)
                    photo_filenames.append(localfile)
        print('Preparation Completed.')
        g = get_douban_task_group(photo_filenames, upload_images_task, group_size=5)
        async_result = g.apply_async()
        print_progress(async_result, "upload images")
