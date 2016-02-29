# -*- coding: utf-8 -*-
import json


def start_parser(text):
    datas = []

    movie_base_datas = json.loads(text).get('subjects', [])
    for movie_base_data in movie_base_datas:
        data = {}
        data['douban_id'] = movie_base_data.get('id')
        data['title'] = movie_base_data.get('title')
        data['cover'] = movie_base_data.get('cover')
        data['cover_x'] = movie_base_data.get('cover_x')
        data['cover_y'] = movie_base_data.get('cover_y')
        data['playable'] = movie_base_data.get('playable')
        data['is_beetle_subject'] = movie_base_data.get('is_beetle_subject')
        data['douban_rate'] = movie_base_data.get('rate')
        data['douban_url'] = movie_base_data.get('url')
        datas.append(data)

    return datas
