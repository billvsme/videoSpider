#!/usr/bin/env python3
import os
import sys
import models
from gevent import monkey;
monkey.patch_socket()
#monkey.patch_os()
from webs import douban
from config import config
from config import sqla; session = sqla['session']

from celery import group
from tqdm import tqdm
from helpers import (get_video_douban_ids,
                     get_celebrity_douban_ids,
                     get_animation_bilibili_ids)
from tasks import (douban_movie_base_task,
                   douban_movie_full_task,
                   douban_celebrity_full_task,
                   bilibili_animation_base_task,
                   bilibili_animation_full_task,
                   down_video_images_task,
                   down_celebrity_images_task,
                   upload_images_task,
                   whoosh_task,
                   get_task_group_by_id)

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
        print('Preparing get video from douban, please wait, about 1 min...(no progress bar)')
        douban_movie_base_task.delay(20).get()
        print('Preparation Completed.')
        
        expression = models.Video.is_detail == False
        douban_ids = list(get_video_douban_ids(expression))

        g = get_task_group_by_id(douban_ids, douban_movie_full_task)

        print('Start get movie full data fron douban:')
        async_result = g.apply_async()
        print_progress(async_result, 'get douban video full data')

        print('Preparing get animation from bilibili, please wait, about 1 min...(no progress bar)')
        bilibili_animation_base_task.delay(20).get()
        print('Preparation Completed.')

        expression = ((models.Animation.is_detail == False) &
                     (models.Animation.bilibili_id != None))
        bilibili_ids = list(get_animation_bilibili_ids(expression))

        g = get_task_group_by_id(bilibili_ids, bilibili_animation_full_task)
        print('Start get animation full data fron bilibili:')
        async_result = g.apply_async()
        print_progress(async_result, 'get bilibili animation full data')

        

    if sys.argv[1] == 'celebrity':
        print('Start get celebrity data:')

        expression = models.Celebrity.is_detail == False
        douban_ids = list(get_celebrity_douban_ids(expression))

        g = get_task_group_by_id(douban_ids, douban_celebrity_full_task)
        async_result = g.apply_async()
        print_progress(async_result, 'get celery data')

    if sys.argv[1] == 'full':
        os.system('python start.py video') 
        os.system('python start.py celebrity') 


    elif sys.argv[1] == 'down-image':
        print('Start down movie images(about use 10+h, 40G):')

        douban_ids = list(get_video_douban_ids())
        g = get_task_group_by_id(douban_ids, down_video_images_task, group_size=5)

        async_result = g.apply_async()
        print_progress(async_result, "down video images")

        douban_ids = list(get_celebrity_douban_ids())
        g = get_task_group_by_id(douban_ids, down_celebrity_images_task, group_size=5)

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
        g = get_task_group_by_id(photo_filenames, upload_images_task, group_size=5)
        async_result = g.apply_async()
        print_progress(async_result, "upload images")

    elif sys.argv[1] == 'whoosh':
        query = session.query(models.Video.id)

        ids = []
        for id_, in query:
            ids.append(id_)

        g = get_task_group_by_id(ids, whoosh_task, group_size=50, model_class=models.Video);
        async_result = g.apply_async()
        print_progress(async_result, "whoosh index")
