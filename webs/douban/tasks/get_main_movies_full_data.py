import requests
import multiprocessing
from gevent.pool import Pool
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from webs import models
from webs import random_str
from webs.douban import parsers
from config import sqla
from . import get_main_movies_base_data


douban_movie_url = 'http://movie.douban.com/subject/'
douban_celebrity_url = 'http://movie.douban.com/celebrity/'
cookies = {
    'bid': ''
}


def create_requests_and_save_datas(douban_id):
    session = sqla['session']
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

    session.commit()

    # If use query.update(data), an error is raised, beacuse movie table is multiple table and we want to update movie table and subject table some columns.

    movie.genres.clear()
    movie.countries.clear()
    movie.languages.clear()
    session.commit()

    for k, v in data.items():
        if k == 'genres':
            for movie_genre in v:
                try:
                    movie_genre_obj = models.MovieGenre(**movie_genre)
                    session.add(movie_genre_obj)
                    session.commit()    
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    movie_genre_obj = session.query(models.MovieGenre).filter_by(name=movie_genre['name']).one()
                movie.genres.append(movie_genre_obj)
        elif k == 'countries':
            for movie_country in v:
                try:
                    movie_country_obj = models.MovieCountry(**movie_country)
                    session.add(movie_country_obj)
                    session.commit()
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    movie_country_obj = session.query(models.MovieCountry).filter_by(name=movie_country['name']).one()
                movie.countries.append(movie_country_obj)
        elif k == 'languages':
            for movie_language in v:
                try:
                    movie_language_obj = models.MovieLanguage(**movie_language)
                    session.add(movie_language_obj)
                    session.commit()
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    movie_language_obj = session.query(models.MovieLanguage).filter_by(name=movie_language['name']).one()
                movie.languages.append(movie_language_obj)
        session.commit()

    '''Why set other value not in above for cycle?
    Beacuse above "for cycle" have rollback.
    '''
    for k, v in data.items():
        if k!= 'genres' and k!='countries' and k!='languages':
            if k == 'aliases' or k == 'thumbnail_photos':
                v = str(v)
            setattr(movie, k, v)

    session.commit()

    # save photo
    r = requests.get(douban_movie_url + str(douban_id) + '/all_photos', cookies=cookies, timeout=10)
    data = parsers.photo.start_parser(r.text)

    for k, v in data.items():
        v = str(v)
        setattr(movie, k, v)

    session.commit()

    print(','.join(
        ['movie', douban_id, movie.title]
    ))



def task(douban_ids, pool_number):
    #engine.dispose()
    pool = Pool(pool_number)

    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id,
        )

    pool.join()
