# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def get_celebrity_info(node):
    celebrity_nodes = node.next_sibling.next_sibling.find_all('a')
    celebrities = [
        {
            'name': celebrity.string,
            'douban_id':
            re.findall(r'\d+', celebrity['href'])[0]
            if re.match(r'/celebrity/\d+/', celebrity['href']) else None
        } for celebrity in celebrity_nodes
    ]

    return celebrities


def get_movie_info(node_dict):
    movie_info = {}
    if '导演' in node_dict:
        movie_info['directors'] = get_celebrity_info(node_dict['导演'])

    if '编剧' in node_dict:
        movie_info['playwrights'] = get_celebrity_info(node_dict['编剧'])

    if '主演' in node_dict:
        movie_info['actors'] = get_celebrity_info(node_dict['主演'])

    if '类型' in node_dict:
        genres = []
        node = node_dict['类型']
        node = node.next_sibling
        while(node.name != 'br'):
            if node.name == 'span':
                genres.append(
                        {
                            'name': node.string
                        }
                )
            node = node.next_sibling

        movie_info['genres'] = genres

    if '官方网站' in node_dict:
        movie_info['official_site'] = \
                node_dict['官方网站'].next_sibling.next_sibling.get('href')

    if '制片国家/地区' in node_dict:
        movie_info['countries'] = [
            {
                'name': name.strip()
            } for name in node_dict['制片国家/地区'].next_sibling.string.split('/')
        ]

    if '语言' in node_dict:
        movie_info['languages'] = [
            {
                'name': name.strip()
            } for name in node_dict['语言'].next_sibling.string.split('/')
        ]

    if '上映日期' in node_dict:
        movie_info['pubdate'] = \
                node_dict['上映日期'].next_sibling.next_sibling.string

    if '片长' in node_dict:
        movie_info['duration'] = \
                node_dict['片长'].next_sibling.next_sibling.string

    if '又名' in node_dict:
        movie_info['aliases'] = [
            name.strip()
            for name in node_dict['又名'].next_sibling.string.split('/')
        ]

    if 'IMDb链接' in node_dict:
        movie_info['imdb_number'] = \
                node_dict['IMDb链接'].next_sibling.next_sibling.string

    if '集数' in node_dict:
        total_count = node_dict['集数'].next_sibling.string.strip()
        movie_info['total_count'] = total_count

    return movie_info


def start_parser(text):
    data = {
        'title': '',
    }

    s = BeautifulSoup(text, "lxml")

    data['title'] = s.select('#content h1 span')[0].string
    data['douban_rate'] = s.select('.rating_num')[0].string
    data['thumbnail_photos'] = [
        photo.get('src')
        for photo in s.find(id='related-pic').find_all('img')
    ]
    if s.find(property='v:summary'):
        data['summary'] = s.find(property='v:summary').string

    info_node_dict = {}
    info_nodes = s.select('.pl')
    for node in info_nodes:
        dict_key = node.string
        if dict_key is not None:
            dict_key = dict_key[:-1] if dict_key.endswith(':') else dict_key
            info_node_dict[dict_key] = node

    data.update(get_movie_info(info_node_dict))

    return data
