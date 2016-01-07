import requests

from parsers import models
from parsers import random_str
from parsers import session


douban_movie_tag_api_url = "http://movie.douban.com/j/search_tags"

cookies = {
    'bid':  random_str(11)
}


douban_ids = set()

for x, in session.query(models.Subject.douban_id).all():
    douban_ids.add(x)


def get_douban_base_movies(url, *args, **kwargs):
    r = requests.get(url, params=kwargs, cookies=cookies)
    movie_base_datas = r.json().get('subjects')


    for movie_base_data in movie_base_datas:
        douban_id = movie_base_data.get('id')
        if douban_id in douban_ids:
            continue
        movie = models.Movie(
            douban_id=movie_base_data.get('id'),
            title=movie_base_data.get('title'),
            image=movie_base_data.get('cover'),
            cover=movie_base_data.get('cover_x'),
            cover_x=movie_base_data.get('cover_x'),
            cover_y=movie_base_data.get('cover_y'),
            playable=movie_base_data.get('playable'),
            is_beetle_subject=movie_base_data.get('is_beetle_subject'),
            rate=movie_base_data.get('rate'),
            douban_url=movie_base_data.get('url'),
            subtype=kwargs.get('type'),
            tag=kwargs.get('tag'),
            sort=kwargs.get('sort')
        )

        session.add(movie)
        session.commit()
        douban_ids.add(douban_id)
        print(douban_id, movie_base_data.get('title'))
