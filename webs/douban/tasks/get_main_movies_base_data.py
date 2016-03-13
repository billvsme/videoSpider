# -*- coding: utf-8 -*-
import requests
import gevent
import models

from gevent.pool import Pool
from helpers import random_str, get_video_douban_ids
from webs.douban import parsers
from config import sqla


types = ['movie', 'tv']
sorts = ['recommend', 'time', 'rank']
tags_dict = {
    'tv': ['热门', '美剧', '英剧', '韩剧', '日剧', '国产剧', '港剧', '日本动画'],
    'movie': ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片',
              '华语', '欧美', '韩国', '日本', '动作', '喜剧', '爱情',
              '科幻', '悬疑', '恐怖', '动画']
}

douban_movie_api_url = 'http://movie.douban.com/j/search_subjects/'
cookies = {
    'bid': ''
}


def create_requests_and_save_datas(type, tag, sort):
    session = sqla['session']
    cookies['bid'] = random_str(11)
    params = {
        'type': type,
        'tag': tag,
        'sort': sort,
        'page_limit': 2000,
        'page_start': 0
    }

    r = requests.get(
            douban_movie_api_url,
            params=params,
            cookies=cookies,
            timeout=20
        )

    if r.status_code != 200:
        return
    datas = parsers.douban_api.start_parser(r.text)

    for data in datas:
        douban_id = data.get('douban_id')
        if douban_id in video_douban_ids:
            continue
        data['subtype'] = type
        data['crawler_tag'] = tag
        data['crawler_sort'] = sort

        if type == 'movie':
            video = models.Movie(**data)
        elif type == 'tv' and tag == '日本动画':
            video = models.Animation(**data)
        else:
            video = models.TV(**data)
        session.add(video)
        session.commit()
        video_douban_ids.add(douban_id)
        print(','.join(
                [douban_id, data.get('title')]
            ))


def task(pool_number, types=types, tags_dict=tags_dict, sorts=sorts):
    video_douban_ids = set(get_video_douban_ids())
    global video_douban_ids

    pool = Pool(pool_number)

    for type in types:
        for tag in tags_dict[type]:
            for sort in sorts:
                pool.spawn(
                    create_requests_and_save_datas,
                    type=type,
                    tag=tag,
                    sort=sort
                )
    pool.join()

    return list(video_douban_ids)
