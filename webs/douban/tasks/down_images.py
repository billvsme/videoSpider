import ast
import requests
from config import sqla
from gevent.pool import Pool
from webs import random_str
from webs import models

cookies = {
        'bid': ''
}

def down(url, path):
    cookies['bid'] = random_str(11)
    r = requests.get(url, cookies=cookies, timeout=10)
    with open(path, 'wb') as f:
        f.write(r.content)


def create_down(str_urls, douban_id, category):
    urls = ast.literal_eval(str_urls)
    base_path = './photos/' + douban_id + '_' + category

    for url in urls:
        down(
            url,
            base_path + '_' + url.split('/')[-1].strip('?')
        )

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


    down(cover_url, './photos/'+douban_id+'_cover_'+cover_url.split('/')[-1].strip('?'))

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
