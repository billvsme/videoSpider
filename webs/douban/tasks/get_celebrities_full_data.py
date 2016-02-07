import models
import requests
import multiprocessing

from helpers import random_str
from resource import session, engine
from gevent.pool import Pool
from webs.douban import parsers


douban_celebrity_url = 'http://movie.douban.com/celebrity/'
cookies = {
        'bid': ''
}

def create_requests_and_save_datas(douban_id):
    cookies['bid'] = random_str(11)

    r = requests.get(douban_celebrity_url + str(douban_id), cookies=cookies, timeout=5)

    if r.status_code != 200:
        return

    data = parsers.celebrity.start_parser(r.text)

    celebrity = session.query(models.Celebrity).filter_by(douban_id=douban_id).one()

    for key in list(data.keys()):
        if type(data[key]) == list:
            data[key] = str(data[key])

    for k, v in data.items():
        setattr(celebrity, k, v)

    session.commit()
    print('celebrity', douban_id, data['name'])


def process_start(douban_ids, pool_number):
    engine.dispose()

    pool = Pool(pool_number)


    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id,
        )

    pool.join()


def start_work(process_number=None, pool_number=50):
    celebrity_douban_ids = []
    
    for celebrity_douban_id, in session.query(models.Celebrity.douban_id):
        celebrity_douban_ids.append(celebrity_douban_id)

    celebrity_size = len(celebrity_douban_ids)

    p = multiprocessing.Pool(processes=process_number)
    process_number = p._processes
    for x in range(0, celebrity_size, celebrity_size//process_number+1):
        p.apply_async(process_start, args=(celebrity_douban_ids[x:x+celebrity_size//process_number], pool_number))

    p.close()
    p.join()
