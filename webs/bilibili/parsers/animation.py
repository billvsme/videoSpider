# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def get_animation_info(node_dict):
    animation_info = {}

    if 'info-detail' in node_dict:
        animation_info['pubdate'] = node_dict['info-detail'].select(
                                        '.info-detail-item-date em'
                                    )[0].string
        animation_info['country'] = node_dict['info-detail'].select(
                                        '.info-detail-item em'
                                    )[1].string
    if 'info-cv' in node_dict:
        animation_info['cv'] = [
            node.text[1:]
            for node in node_dict['info-cv'].select('.info-cv-item')
        ]

    if 'info-style' in node_dict:
        animation_info['genres'] = [
            {
                'name': node.string
            } for node in node_dict['info-style'].select('.info-style-item')
        ]

    if 'info-desc-wrp' in node_dict:
        animation_info['summary'] = node_dict['info-desc-wrp'].find(
                                        class_='info-desc'
                                    ).string

    return animation_info


def start_parser(text):
    data = {}

    s = BeautifulSoup(text, 'lxml')

    data['title'] = s.find(class_='info-title').string
    data['cover'] = s.find(class_='bangumi-preview').img.get('src')
    data['aliases'] = s.select('.info-syn-words')
    classes = [
        'info-detail',
        'info-tag',
        'info-cv',
        'info-style',
        'info-desc-wrp',
    ]

    node_dict = {}
    for class_ in classes:
        node = s.find(class_=class_)
        if node is not None:
            node_dict[class_] = node

    data.update(get_animation_info(node_dict))

    return data
