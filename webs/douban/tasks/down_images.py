import ast
import requests
from config import sqla
from gevent.pool import Pool
from webs import random_str
from webs import models

cookies = {
        'bid': ''
}

def down(url, filename):
    r = requests.get(url)
    with open('./photos/'+filename, 'wb') as f:
        f.write(r.content)

def create_requests_and_save_datas(douban_id):
    session = sqla['session']
    cookies['bid'] = random_str(11)
    subject = session.query(models.Subject).filter_by(douban_id=douban_id).one()

    cover_url = subject.cover
    photos_url = subject.photos
    if type(photos_url) == str:
        photos_url =  ast.literal_eval(photos_url)

    down(cover_url, douban_id+'_cover_'+cover_url.split('/')[-1].strip('?'))
    for photo_url in photos_url:
        down(photo_url, douban_id+'_photos_'+photo_url.split('/')[-1].strip('?'))
        

def task(douban_ids, pool_number):
    pool = Pool(pool_number)

    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id
        )

    pool.join()
