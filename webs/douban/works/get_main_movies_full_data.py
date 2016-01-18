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

    movie = session.query(models.Movie).filter_by(douban_id=douban_id).one()

    directors = data.pop('directors', [])
    director_douban_ids = set(director['douban_id'] for director in directors)
    playwrights = data.pop('playwrights', [])
    playwright_douban_ids = set(playwright['douban_id'] for playwright in playwrights)
    actors = data.pop('actors', [])
    actor_douban_ids = set(actor['douban_id'] for actor in actors)
    celebrities = directors + playwrights + actors
    celebrity_douban_ids = director_douban_ids & playwright_douban_ids & actor_douban_ids

    exist_celebrity_query = session.query(
                               models.Celebrity
                           ).filter(models.Celebrity.douban_id.in_(celebrity_douban_ids))

    exist_celebrity_douban_ids = set()
    douban_id_celebrity_obj_dict = {}

    for celebrity_obj in exist_celebrity_query:
        exist_celebrity_douban_ids.add(celebrity_obj.douban_id)
        douban_id_celebrity_obj_dict[celebrity_obj.douban_id] = celebrity_obj

    for celebrity in celebrities:
        celebrity_douban_id = celebrity['douban_id']
        if celebrity_douban_id is None:
            continue
        if celebrity_douban_id not in exist_celebrity_douban_ids:
            celebrity_obj = models.Celebrity(**celebrity)
            session.add(celebrity_obj)
            session.flush()
            douban_id_celebrity_obj_dict[celebrity_douban_id] = celebrity_obj
            exist_celebrity_douban_ids.add(celebrity_douban_id)

    movie.directors.clear()
    movie.playwrights.clear()
    movie.actors.clear()

    for celebrity_douban_id, celebrity_obj  in douban_id_celebrity_obj_dict.items():
        if celebrity_douban_id in director_douban_ids:
            movie.directors.append(celebrity_obj)
        if celebrity_douban_id in playwright_douban_ids:
            movie.playwrights.append(celebrity_obj)
        if celebrity_douban_id in actor_douban_ids:
            movie.actors.append(celebrity_obj)
    
    for key in list(data.keys()):
        if type(data[key]) == list:
            data[key] = str(data[key])

    # If use query.update(data), an error is raised, beacuse movie table is multiple table and we want to update movie table and subject table some columns.
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
