import gipc
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
    r = requests.get(douban_movie_url + str(douban_id), cookies=cookies, timeout=10)

    data = parsers.douban_movie_page(r)

    if 'directors' in data:
        data.pop('directors')
    if 'playwrights' in data:
        data.pop('playwrights')
    if 'actors' in data:
        data.pop('actors')

    for key in list(data.keys()):
        if type(data[key]) == list:
            data[key] = str(data[key])

    # If use query.update(data), an error is raised, beacuse movie table is multiple table and we want to update movie table and subject table some columns.
    movie = session.query(models.Movie).filter_by(douban_id=douban_id).one()

    for k, v in data.items():
        setattr(movie, k, v)

    session.commit()
    print(douban_id, movie.title)


def process_start(ids):
    pool = Pool(100)

    for douban_id in ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id
        )

    pool.join()


def start():
    get_main_movies_base_data.start()
    all_ids = list(get_main_movies_base_data.douban_ids)
    l = len(all_ids)

    processes = []
    for x in range(0, l, l//4+1):
        processes.append(
                gipc.start_process(target=process_start, args=(all_ids[x: x+l//4],))
        )

    for process in processes:
        process.join()
