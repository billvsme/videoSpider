import requests
import gevent
from gevent import monkey
from gevent.pool import Pool

from . import parsers
from . import session
from . import models


monkey.patch_socket()

types = ['movie', 'tv']
sorts = ['recommend', 'time', 'rank']
douban_movie_api_url = 'http://movie.douban.com/j/search_subjects/'
douban_movie_url = 'http://movie.douban.com/subject/'

tags_dict = parsers.douban.get_douban_tags_dict()


def movie_base():
    threads = set()
    for type in types:
        for tag in tags_dict[type]:
            for sort in sorts:
                threads.add(gevent.spawn(
                    parsers.douban.get_douban_base_movies,
                    douban_movie_api_url,
                    type=type,
                    tag=tag, 
                    sort=sort,
                    page_limit=2000,
                    page_start=0
                ))

    gevent.joinall(threads)


def full():
    douban_ids = set()
    for x, in session.query(models.Subject.douban_id).all():
        douban_ids.add(x)

    pool = Pool(150)
    for douban_id in range(1291543, 26687572):
        if douban_id in douban_ids:
            continue
        pool.spawn(parsers.douban.get_douban_movies, douban_movie_url + str(douban_id))
    pool.join()


def start():
    movie_base()
    print("movie_base end =============")
    full()
    print("all end =====================")
