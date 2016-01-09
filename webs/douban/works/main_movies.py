import requests
import gevent
from gevent import monkey
from gevent.pool import Pool

from webs import session
from webs import models
from webs import random_str

from webs.douban import parsers

monkey.patch_socket()


types = ['movie', 'tv']
sorts = ['recommend', 'time', 'rank']
tags_dict = {
    'tv': ['热门', '美剧', '英剧', '韩剧', '日剧', '国产剧', '港剧', '日本动画'],
    'movie': ['热门', '最新', '经典', '可播放', '豆瓣高分', '冷门佳片', '华语', '欧美', '韩国','日本', '动作', '喜剧', '爱情', '科幻', '悬疑', '恐怖', '动画']
}

douban_movie_api_url = 'http://movie.douban.com/j/search_subjects/'
douban_movie_url = 'http://movie.douban.com/subject/'

cookies = {
    'bid': ''
}

douban_ids = set()

for x, in session.query(models.Subject.douban_id).all():
    douban_ids.add(x)


def create_requests_and_save_datas(type, tag, sort):
    cookies['bid'] = random_str(11)
    params = {
        'type': type,
        'tag': tag,
        'sort': sort,
        'page_limit': 2000,
        'page_start': 0
    }

    r = requests.get(douban_movie_api_url, params=params, cookies=cookies)
    datas = parsers.get_douban_main_movies_base_data(r)

    for data in datas:
        douban_id = data.get('douban_id')
        if douban_id in douban_ids:
            continue
        data['subtype'] = type
        data['tag'] = tag
        data['sort'] = sort

        movie = models.Movie(**data)
        session.add(movie)
        session.commit()
        douban_ids.add(douban_id)
        print(douban_id, data.get('title'))

def start():
    threads = set() 
    for type in types:
        for tag in tags_dict[type]:
            for sort in sorts:
                threads.add(gevent.spawn(
                    create_requests_and_save_datas,
                    type=type,
                    tag=tag,
                    sort=sort
                ))

    gevent.joinall(threads)
