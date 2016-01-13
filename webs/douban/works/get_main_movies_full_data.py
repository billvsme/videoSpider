import requests
from gevent.pool import Pool

from webs import session
from webs import models
from webs import random_str
from webs.douban import parsers

from . import get_main_movies_base_data


douban_movie_url = 'http://movie.douban.com/subject/'
cookies = {
    'bid': ''
}


def create_requests_and_save_datas(douban_id):
    cookies['bid'] = random_str(11)
    r = requests.get(douban_movie_url + str(douban_id), cookies=cookies)
    data = parsers.douban_movie_page(r)
    print(data)


def start():
    get_main_movies_base_data.start()
    pool = Pool(150)

    for douban_id in list(get_main_movies_base_data.douban_ids):
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id
        )

    pool.join()
