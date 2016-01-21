import gipc
import requests
from gevent.pool import Pool
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from webs import models
from webs import random_str
from webs.douban import parsers
from resource import session, engine
from . import get_main_movies_base_data


douban_movie_url = 'http://movie.douban.com/subject/'
douban_celebrity_url = 'http://movie.douban.com/celebrity/'
cookies = {
    'bid': ''
}


def create_requests_and_save_datas(douban_id):
    cookies['bid'] = random_str(11)
    r = requests.get(douban_movie_url + str(douban_id), cookies=cookies, timeout=10)

    if r.status_code != 200:
        return

    data = parsers.movie.start_parser(r.text)
    data['douban_url'] = r.url

    directors = data.pop('directors', [])
    director_douban_ids = set(director['douban_id'] for director in directors)
    playwrights = data.pop('playwrights', [])
    playwright_douban_ids = set(playwright['douban_id'] for playwright in playwrights)
    actors = data.pop('actors', [])
    actor_douban_ids = set(actor['douban_id'] for actor in actors)
    celebrities = directors + playwrights + actors
    celebrity_douban_ids = director_douban_ids | playwright_douban_ids | actor_douban_ids

    douban_id_celebrity_obj_dict = {}

    for celebrity in celebrities:
        celebrity_douban_id = celebrity['douban_id']
        if celebrity_douban_id is not None:
            try:
                celebrity_obj = models.Celebrity(**celebrity)
                session.add(celebrity_obj)
                session.commit()
            except (IntegrityError, InvalidRequestError):
                session.rollback()
                celebrity_obj = session.query(models.Celebrity).filter_by(douban_id=celebrity_douban_id).first()
            douban_id_celebrity_obj_dict[celebrity_douban_id] = celebrity_obj

    movie = session.query(models.Movie).filter_by(douban_id=douban_id).one()
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
    print('movie', douban_id, movie.title)


def process_start(douban_ids, pool_number):
    engine.dispose()
    pool = Pool(pool_number)

    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id,
        )

    pool.join()


def start_work(process_number=4, pool_number=50):
    movie_douban_ids = []
    for movie_douban_id, in session.query(models.Movie.douban_id).all():
        movie_douban_ids.append(movie_douban_id)

    movie_douban_ids = movie_douban_ids
    l = len(movie_douban_ids)

    processes = []
    for x in range(0, l, l//process_number+1):
        processes.append(
                gipc.start_process(target=process_start, args=(movie_douban_ids[x: x+l//process_number],pool_number))
        )

    for process in processes:
        process.join()
