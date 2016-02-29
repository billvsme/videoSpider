# -*- coding: utf-8 -*-
import json


def start_parser(text):
    datas = []
    animation_base_datas = json.loads(text)['result']['list']
    for animation_base_data in animation_base_datas:
        data = {}

        data['bilibili_id'] = animation_base_data['season_id']
        data['title'] = animation_base_data['title']
        data['cover'] = animation_base_data['cover']
        data['total_count'] = int(animation_base_data['total_count'])
        datas.append(data)

    return datas
