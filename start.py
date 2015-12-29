#!/usr/bin/env python3
import requests
import pyquery
import models
import configparser
from models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


base_url = "http://movie.douban.com/j/search_subjects"

# url params
tags = ["热门", "美剧", "英剧", "韩剧", "日剧", "港剧", "日本动画"]
sorts = ["recommend", "time", "rank"]
params = {
    "type": "tv",
    "tag": "热门",
    "sort": "recommend",
    "page_limit": "2000",
    "page_start": "0"
}


# read config.ini file
config = configparser.ConfigParser()
config.read('./config.ini')

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

for tag in tags:
    params['tag'] = tag
    for sort in sorts:
        params['sort'] = sort
        r = requests.get(base_url, params=params)
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
            douban_ids.add(tv_data.get("id"))
            print(len(douban_ids), tv_data.get('title'))

        session.commit()
