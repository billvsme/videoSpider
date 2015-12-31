#!/usr/bin/env python3
import configparser
import gevent
import os
import pyquery
import requests
import models
from models import Base
from gevent import monkey
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# use gevent
monkey.patch_socket()

get_subject_url = "http://movie.douban.com/j/search_subjects"
get_tag_url = "http://movie.douban.com/j/search_tags"

# url params
types = ["movie", "tv"]
tags = ["热门", "美剧", "英剧", "韩剧", "日剧", "港剧", "日本动画"]
sorts = ["recommend", "time", "rank"]


# get tags
def get_tags(type_):
    r = requests.get(get_tag_url, {"type": type_})
    tags = r.json().get("tags")

    return tags

tags_dict = {
    type_: get_tags(type_) for type_ in types
}


# read config.ini file
config = configparser.ConfigParser()
if os.path.exists('./config.ini'):
    config.read('./config.ini')
else:
    config.read('./config_dev.ini')

# create database engine use config database url
engine = create_engine(
    config['database']['database_url'],
    echo=config['database'].getboolean('test') or False
)

# create table
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

subjects = session.query(models.Subject)

douban_ids = set()

for subject in subjects:
    douban_ids.add(subject.douban_id)

print("already in:", len(douban_ids))


def get_tv_datas(type_, tag, sort):
    params = {
        "type": type_,
        "tag": tag,
        "sort": sort,
        "page_limit": "2000",
        "page_start": "0"
    }

    r = requests.get(get_subject_url, params=params)
    tv_json = r.json()
    tv_datas = tv_json['subjects']

    for tv_data in tv_datas:
        if tv_data.get('id') in douban_ids:
            continue
        subject = models.Subject(
                douban_id=tv_data.get('id'),
                title=tv_data.get('title'),
                cover=tv_data.get('cover'),
                cover_x=tv_data.get('cover_x'),
                cover_y=tv_data.get('cover_y'),
                playable=tv_data.get('playable'),
                is_new=tv_data.get('is_new'),
                is_beetle_subject=tv_data.get('is_beetle_subject'),
                rate=tv_data.get('rate'),
                douban_url=tv_data.get('url')
        )
        session.add(subject)
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
