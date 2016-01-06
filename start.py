#!/usr/bin/env python3
import gevent
import os
import pyquery
import random
import requests
import string
import models
from config import config
from gevent import monkey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from helpers import random_str
from resource import session

# use gevent
monkey.patch_socket()


get_subject_url = "http://movie.douban.com/j/search_subjects"
get_tag_url = "http://movie.douban.com/j/search_tags"

# url params
types = ["movie", "tv"]
tags = ["热门", "美剧", "英剧", "韩剧", "日剧", "港剧", "日本动画"]
sorts = ["recommend", "time", "rank"]

# cookies
cookies = {
    "bid": random_str(11),
}

# get tags
def get_tags(type_):
    r = requests.get(get_tag_url, {"type": type_}, cookies=cookies)
    tags = r.json().get("tags")

    return tags

tags_dict = {
    type_: get_tags(type_) for type_ in types
}


douban_ids = set()

for x,in session.query(models.Subject.id).all():
    douban_ids.add(x)


print("already in:", len(douban_ids))


def get_tv_datas(type_, tag, sort):
    params = {
        "type": type_,
        "tag": tag,
        "sort": sort,
        "page_limit": "2000",
        "page_start": "0"
    }

    r = requests.get(get_subject_url, params=params, cookies=cookies)
    tv_json = r.json()
    tv_datas = tv_json['subjects']

    for tv_data in tv_datas:
        if tv_data.get('id') in douban_ids:
            continue
        movie = models.Movie(
                douban_id=tv_data.get('id'),
                title=tv_data.get('title'),
                image=tv_data.get('cover'),
                cover=tv_data.get('cover'),
                cover_x=tv_data.get('cover_x'),
                cover_y=tv_data.get('cover_y'),
                playable=tv_data.get('playable'),
                is_new=tv_data.get('is_new'),
                is_beetle_subject=tv_data.get('is_beetle_subject'),
                rate=tv_data.get('rate'),
                douban_url=tv_data.get('url'),
                subtype=type_,
                tag=tag,
                sort=sort
        )
        session.add(movie)
        session.flush()
        douban_ids.add(tv_data.get("id"))
        print(len(douban_ids), tv_data.get('title'))


threads = set()
for type_ in types:
    for tag in tags_dict[type_]:
        for sort in sorts:
            threads.add(gevent.spawn(get_tv_datas, type_, tag, sort))

gevent.joinall(threads)

session.commit()
print("now in:", len(douban_ids))


subject_url = "http://movie.douban.com/subject/"
book_url = "http://book.douban.com/subject/"
 

print("end base crawler============")

 
from gevent.pool import Pool
from pyquery import PyQuery as pq
from parsers import get_douban_movie

pool = Pool(150)
for douban_id in range(1291543, 26687572):
    if douban_id in douban_ids:
        continue
    pool.spawn(get_douban_movie, douban_id)

print("====================")
pool.join()
