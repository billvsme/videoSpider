import requests

from parsers import random_str
from parsers import session


douban_movie_tag_api_url = "http://movie.douban.com/j/search_tags"

types = ['movie', 'tv']
sorts = ['recommend', 'time', 'rank']

cookies = {
    'bid':  random_str(11)
}


def get_tags(type):
    cookies['bid'] = random_str(11)
    r = requests.get(douban_movie_tag_api_url, {'type': type}, cookies=cookies)
    tags = r.json().get('tags')

    return tags

tags_dict = {
    type: get_tags(type) for type in types
}

def get_douban_tags_dict():
    return tags_dict
