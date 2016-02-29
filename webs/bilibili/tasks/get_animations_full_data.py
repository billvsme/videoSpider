# -*- coding: utf-8 -*-
import requests
import models

from config import sqla
from helpers import random_str
from gevent.pool import Pool
from webs.bilibili import parsers
from sqlalchemy.exc import IntegrityError, InvalidRequestError


bilibili_animation_url = 'http://www.bilibili.com/bangumi/i/'
cookies = {
    'sid': ''
}


def create_requests_and_save_datas(bilibili_id):
    session = sqla['session']
    cookies['sid'] = random_str(8)

    r = requests.get(
            bilibili_animation_url + str(bilibili_id),
            cookies=cookies,
            timeout=10
        )

    if r.status_code != 200:
        return

    data = parsers.animation.start_parser(r.text)

    animation = session.query(models.Animation).filter_by(
                    bilibili_id=bilibili_id
                ).one()

    genre_class = models.AnimationGenre
    for k, v in data.items():
        if k == 'genres':
            for genre in v:
                try:
                    genre_obj = genre_class(**genre)
                    session.add(genre_obj)
                    session.commit()
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    genre_obj = session.query(genre_class).filter_by(
                                    name=genre['name']
                                ).one()
                animation.genres.append(genre_obj)

    for k, v in data.items():
        if k != 'genres':
            if type(v) == list:
                v = str(v)
            setattr(animation, k, v)

    animation.is_detail = True
    session.commit()

    print(','.join(
        [bilibili_id, data.get('title')]
    ))


def task(bilibili_ids, pool_number):
    pool = Pool(pool_number)

    for bilibili_id in bilibili_ids:
        pool.spawn(
            create_requests_and_save_datas,
            bilibili_id=bilibili_id,
        )

    pool.join()
