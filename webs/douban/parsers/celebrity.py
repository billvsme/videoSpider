# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def get_celebrity_info(info_node_dict):
    celebrity_info = {}
    if '性别' in info_node_dict:
        celebrity_info['sex'] = \
                info_node_dict['性别'].span.next_sibling.string.strip(': \n')
    if '星座' in info_node_dict:
        celebrity_info['constellation'] = \
                info_node_dict['星座'].span.next_sibling.string.strip(': \n')
    if '出生日期' in info_node_dict:
        celebrity_info['birthday'] = \
                info_node_dict['出生日期'].span.next_sibling.string.strip(': \n')
    if '出生地' in info_node_dict:
        celebrity_info['born_place'] = \
                info_node_dict['出生地'].span.next_sibling.string.strip(': \n')
    if '职业' in info_node_dict:
        celebrity_info['professions'] = \
                info_node_dict['职业'].span.next_sibling.string.strip(': \n')
    if '更多中文名' in info_node_dict:
        celebrity_info['aliases'] = \
                info_node_dict['更多中文名'].span.next_sibling.string.strip(': \n')
    if '更多外文名' in info_node_dict:
        celebrity_info['aliases_en'] = \
                info_node_dict['更多外文名'].span.next_sibling.string.strip(': \n')
    if '家庭成员' in info_node_dict:
        celebrity_info['family'] = \
                info_node_dict['家庭成员'].span.next_sibling.string.strip(': \n')
    if 'imdb编号' in info_node_dict:
        celebrity_info['imdb_number'] = \
                info_node_dict['imdb编号'].find('a').string

    return celebrity_info


def start_parser(text):
    data = {}

    s = BeautifulSoup(text, 'lxml')

    data['name'] = s.select('#content h1')[0].string
    data['thumbnail_cover'] = s.select('.nbg img')[0].get('src')
    data['cover'] = data['thumbnail_cover'].replace('/medium', '/large')
    data['summary'] = s.select('#intro .bd')[0].text.strip('\n\u3000 ')
    data['thumbnail_photos'] = [
        photo.get('src')
        for photo in s.select('#intro + .mod')[0].find_all('img')
    ]
    data['photos'] = [
        photo.replace('/albumicon', '/photo')
        for photo in data['thumbnail_photos']
    ]

    info_node_dict = {}
    info_nodes = s.find(class_='info').find_all('li')
    for node in info_nodes:
        dict_key = node.span.string
        if dict_key is not None:
            info_node_dict[dict_key] = node

    data.update(get_celebrity_info(info_node_dict))

    return data
