# -*- coding: utf-8 -*-
import os
import sys
import models
from gevent import monkey
from webs import douban
from config import config, video_ix
from config import sqla

from celery import group
from tqdm import tqdm
from helpers import (get_video_douban_ids,
                     get_video_ids,
                     get_celebrity_douban_ids,
                     get_animation_bilibili_ids,
                     progress)
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

monkey.patch_socket()


@progress(
    start_info='Preparing get video from douban, \
please wait, about 1 min...(no progress bar)',
    end_info='Preparation Completed.')
def douban_video_prepare():
    douban_movie_base_task.delay(20).get()


@progress(
        start_info='Start get movie full data fron douban:',
        desc='get douban video full data')
def douban_video_full_data():
    expression = models.Video.is_detail == False
    douban_ids = list(get_video_douban_ids(expression))

    g = get_task_group_by_id(douban_ids, douban_movie_full_task)

    async_result = g.apply_async()

    return async_result


@progress(
        start_info='Preparing get animation from bilibili, \
please wait, about 1 min...(no progress bar)',
        end_info='Preparation Completed.')
def bilibili_animation_prepare():
        bilibili_animation_base_task.delay(20).get()


@progress(
        start_info='Start get animation full data fron bilibili:',
        desc='get bilibili animation full data')
def bilibili_animation_full_data():
    expression = (
        (models.Animation.is_detail == False) &
        (models.Animation.bilibili_id != None)
    )
    bilibili_ids = list(get_animation_bilibili_ids(expression))
    g = get_task_group_by_id(bilibili_ids, bilibili_animation_full_task)
    async_result = g.apply_async()

    return async_result


@progress(
    start_info='Start get celebrity data:',
    desc='get celery data')
def douban_celebrity_data():
    expression = models.Celebrity.is_detail == False
    douban_ids = list(get_celebrity_douban_ids(expression))

    g = get_task_group_by_id(douban_ids, douban_celebrity_full_task)
    async_result = g.apply_async()

    return async_result


@progress(
    start_info='Start down video images(about use 10+h, 40G):',
    desc='down video images')
def down_video_images():
    douban_ids = list(get_video_douban_ids())
    g = get_task_group_by_id(douban_ids, down_video_images_task, group_size=5)

    async_result = g.apply_async()

    return async_result


@progress(
    start_info='Start down celebrity images(about use 10+h, 40G):',
    desc='down celebrity images')
def down_celebrity_images():
    douban_ids = list(get_celebrity_douban_ids())
    g = get_task_group_by_id(
            douban_ids, down_celebrity_images_task,
            group_size=5
        )

    async_result = g.apply_async()

    return async_result


@progress(
    start_info='Preparing, please wait, about 1 min...(no progress bar)',
    end_info='Preparation Completed.')
def upload_images_prepare():
    global photo_filenames
    photo_filenames = []
    for dirpath, dirnames, filenames in os.walk(config.get('photo', 'path')):
        print(dirpath)
        if len(filenames) > 0:
            for filename in filenames:
                if filename.startswith('.'):
                    continue
                localfile = os.path.join(dirpath, filename)
                photo_filenames.append(localfile)


@progress(
    start_info='Start upload images to qiniu:',
    desc='upload images')
def upload_images():
    g = get_task_group_by_id(photo_filenames, upload_images_task, group_size=5)
    async_result = g.apply_async()

    return async_result


@progress(desc='whoosh index')
def create_whoosh_index():
    video_douban_ids = list(get_video_ids(models.Video.douban_id != None))
    g = get_task_group_by_id(
        video_douban_ids,
        whoosh_task,
        group_size=50,
        Ix=video_ix,
        model_class=models.Video
    )
    async_result = g.apply_async()

    return async_result


if __name__ == '__main__':
    if sys.argv[1] == 'video':
        douban_video_prepare()
        douban_video_full_data()
        bilibili_animation_prepare()
        bilibili_animation_full_data()

    elif sys.argv[1] == 'celebrity':
        douban_celebrity_data()

    elif sys.argv[1] == 'full':
        os.system('python start.py video')
        os.system('python start.py celebrity')

    elif sys.argv[1] == 'down-image':
        down_video_images()
        down_celebrity_images()

    elif sys.argv[1] == 'upload-image':
        upload_images_prepare()
        upload_images()

    elif sys.argv[1] == 'whoosh':
        create_whoosh_index()
