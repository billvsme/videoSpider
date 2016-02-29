# -*- coding: utf-8 -*-
import requests
import multiprocessing
import models

from gevent.pool import Pool
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from helpers import random_str
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
    r = requests.get(
            douban_movie_url + str(douban_id),
            cookies=cookies,
            timeout=10
        )

    if r.status_code != 200:
        return

    data = parsers.movie.start_parser(r.text)
    data['douban_url'] = r.url

    directors = data.pop('directors', [])
    director_douban_ids = set(director['douban_id'] for director in directors)
    playwrights = data.pop('playwrights', [])
    playwright_douban_ids = set(
                                playwright['douban_id']
                                for playwright in playwrights
                            )
    actors = data.pop('actors', [])
    actor_douban_ids = set(actor['douban_id'] for actor in actors)
    celebrities = directors + playwrights + actors
    celebrity_douban_ids = \
        director_douban_ids | playwright_douban_ids | actor_douban_ids

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
                celebrity_obj = session.query(models.Celebrity).filter_by(
                                    douban_id=celebrity_douban_id
                                ).first()
            douban_id_celebrity_obj_dict[celebrity_douban_id] = celebrity_obj

    video = session.query(models.Video).filter_by(douban_id=douban_id).one()
    video.directors.clear()
    video.playwrights.clear()
    video.actors.clear()

    for (celebrity_douban_id,
         celeBrity_obj) in douban_id_celebrity_obj_dict.items():
        if celebrity_douban_id in director_douban_ids:
            video.directors.append(celebrity_obj)
        if celebrity_douban_id in playwright_douban_ids:
            video.playwrights.append(celebrity_obj)
        if celebrity_douban_id in actor_douban_ids:
            video.actors.append(celebrity_obj)

    session.commit()

    """If use query.update(data), an error is raised,
    beacuse movie table is multiple table and we want to
    update movie table and subject table some columns.
    """

    video.genres.clear()
    video.countries.clear()
    video.languages.clear()
    session.commit()

    table_name = video.__tablename__
    if table_name == 'movies':
        genre_class = models.MovieGenre
    elif table_name == 'tvs':
        genre_class = models.TVGenre
    elif table_name == 'animations':
        genre_class = models.AnimationGenre
    for k, v in data.items():
        if k == 'genres':
            for genre in v:
                try:
                    genre_obj = genre_class(**genre)
                    session.add(genre_obj)
                    session.commit()
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    genre_obj = session.query(genre_class).filter_by(
                                    name=genre['name']
                                ).one()
                video.genres.append(genre_obj)
        elif k == 'countries':
            for country in v:
                try:
                    country_obj = models.Country(**country)
                    session.add(country_obj)
                    session.commit()
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    country_obj = session.query(models.Country).filter_by(
                                      name=country['name']
                                  ).one()
                video.countries.append(country_obj)
        elif k == 'languages':
            for language in v:
                try:
                    language_obj = models.Language(**language)
                    session.add(language_obj)
                    session.commit()
                except (IntegrityError, InvalidRequestError):
                    session.rollback()
                    language_obj = session.query(models.Language).filter_by(
                                       name=language['name']
                                   ).one()
                video.languages.append(language_obj)
        session.commit()

    '''Why set other value not in above for cycle?
    Beacuse above "for cycle" have rollback.
    '''
    for k, v in data.items():
        if k != 'genres' and k != 'countries' and k != 'languages':
            if k == 'aliases' or k == 'thumbnail_photos':
                v = str(v)
            setattr(video, k, v)

    session.commit()

    # parser movie photo
    r = requests.get(
            douban_movie_url + str(douban_id) + '/all_photos',
            cookies=cookies,
            timeout=10
        )
    photo_data = parsers.movie_photo.start_parser(r.text)

    for k, v in photo_data.items():
        v = str(v)
        setattr(video, k, v)

    video.is_detail = True
    session.commit()

    print(','.join(
        [table_name, douban_id, data.get('title')]
    ))


def task(douban_ids, pool_number):
    pool = Pool(pool_number)

    for douban_id in douban_ids:
        pool.spawn(
            create_requests_and_save_datas,
            douban_id=douban_id,
        )

    pool.join()
