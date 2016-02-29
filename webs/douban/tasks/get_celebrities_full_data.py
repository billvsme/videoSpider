# -*- coding: utf-8 -*-
import models
import requests
import multiprocessing

from helpers import random_str
from config import sqla
from gevent.pool import Pool
from webs.douban import parsers


douban_celebrity_url = 'http://movie.douban.com/celebrity/'
cookies = {
        'bid': ''
}


def create_requests_and_save_datas(douban_id):
    session = sqla['session']
    cookies['bid'] = random_str(11)

    r = requests.get(
            douban_celebrity_url + str(douban_id),
            cookies=cookies,
            timeout=5
        )

    if r.status_code != 200:
        return

    data = parsers.celebrity.start_parser(r.text)

    celebrity = session.query(models.Celebrity).filter_by(
                    douban_id=douban_id
                ).one()

    for key in list(data.keys()):
        if type(data[key]) == list:
            data[key] = str(data[key])

    for k, v in data.items():
        setattr(celebrity, k, v)

    celebrity.is_detail = True
    session.commit()
    print(' '.join(
        ['celebrity', douban_id, data['name']]
    ))


def task(douban_ids, pool_number):
    pool = Pool(pool_number)

    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id,
        )

    pool.join()
