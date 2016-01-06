import requests

from parsers import pq
from parsers import models
from parsers import random_str
from parsers import session


douban_movie_url = 'http://movie.douban.com/subject/'
cookies = {
    'bid': random_str(11),
}


def get_douban_movie(douban_id):
    cookies['bid'] = random_str(11)
    r = requests.get(douban_movie_url + str(douban_id), cookies=cookies)
    if r.status_code != 404:
        d = pq(r.text)
        title = d('#content h1 span').text()
        print(douban_id, 'movie', r, title)
        movie = models.Movie(
            title=title
        )
        session.add(movie)
    else:
        print(douban_id, "is book.")
    session.commit()
