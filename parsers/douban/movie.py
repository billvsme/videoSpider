import requests

from parsers import pq
from parsers import models
from parsers import random_str
from parsers import session


douban_movie_url = 'http://movie.douban.com/subject/'
cookies = {
    'bid': '',
}


def get_douban_movies(url):
    cookies['bid'] = random_str(11)
    r = requests.get(url, cookies=cookies)
    if r.status_code != 404:
        d = pq(r.text)
        title = d('#content h1 span').text()
        print(url, 'movie', r, title)
        movie = models.Movie(
            title=title
        )
        session.add(movie)
    else:
        print(url, "is book.")
    session.commit()
