# -*- coding: utf-8 -*-
import requests
import models
from config import sqla
from gevent.pool import Pool

from helpers import random_str, get_animation_bilibili_ids
from webs.bilibili import parsers
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

bilibili_api_url = 'http://www.bilibili.com/api_proxy'

cookies = {
    'sid': ''
}


def create_requests_and_save_datas(page):
    session = sqla['session']
    cookies['sid'] = random_str(8)

    params = {
        'app': 'bangumi',
        'page': page,
        'indexType': 0,
        'pagesize': 30,
        'action': 'site_season_index'
    }

    r = requests.get(
            bilibili_api_url,
            params=params,
            cookies=cookies,
            timeout=10
        )

    if r.status_code != 200:
        return

    text = r.text
    if text == 'null':
        return
    datas = parsers.bilibili_api.start_parser(text)

    for data in datas:
        bilibili_id = data.get('bilibili_id')
        if bilibili_id in animation_bilibili_ids:
            continue
        try:
            t = session.query(models.Animation).filter(
                    models.Animation.title.like('%'+data['title']+'%')
                ).one()
        except NoResultFound:
            animation = models.Animation(**data)
            session.add(animation)
            session.commit()
            print(','.join(
                    [data.get('bilibili_id'), data.get('title')]
                ))
        except MultipleResultsFound:
            pass


def task(pool_number, pages=range(1, 100)):
    animation_bilibili_ids = set(get_animation_bilibili_ids())
    global animation_bilibili_ids

    pool = Pool(pool_number)

    for page in pages:
        pool.spawn(
            create_requests_and_save_datas,
            page=page
        )

    pool.join()

    return animation_bilibili_ids
