import ast
import os
import requests
import models

from config import config, sqla
from gevent.pool import Pool
from helpers import random_str, down


base_path = config.get('photo', 'path')
cookies = {
        'bid': ''
}

'''
def down(url, cookies, path, filename):
    cookies['bid'] = random_str(11)
    r = requests.get(url, cookies=cookies, timeout=10)
    try:
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(r.content)
    except FileNotFoundError:
        os.makedirs(path)
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(r.content)
'''

def create_down(str_urls, douban_id, category):
    urls = ast.literal_eval(str_urls)
    path = os.path.join(base_path, category)

    for url in urls:
        filename = str(douban_id) + '_' + url.split('/')[-1].strip('?')
        cookies['bid'] = random_str(11)
        down(url, cookies, path, filename)

def create_requests_and_save_datas(douban_id):
    session = sqla['session']
    cookies['bid'] = random_str(11)
    subject = session.query(models.Subject).filter_by(douban_id=douban_id).one()

    cover_url = subject.cover
    covers_url = subject.covers
    thumbnail_covers_url = subject.thumbnail_covers
    photos_url = subject.photos
    thumbnail_photos_url = subject.thumbnail_photos
    wallpapers_url = subject.wallpapers
    thumbnail_wallpapers_url = subject.thumbnail_wallpapers


    down(cover_url, cookies, os.path.join(base_path, 'cover'), str(douban_id)+'_'+cover_url.split('/')[-1].strip('?'))

    create_down(covers_url, douban_id, 'covers')
    create_down(thumbnail_covers_url, douban_id, 'thumbnail_covers')
    create_down(photos_url, douban_id, 'photos')
    create_down(thumbnail_photos_url, douban_id, 'thumbnail_photos')
    create_down(wallpapers_url, douban_id, 'wallpapers')
    create_down(thumbnail_wallpapers_url, douban_id, 'thumbnail_wallpapers')
        

def task(douban_ids, pool_number):
    pool = Pool(pool_number)

    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id
        )

    pool.join()
