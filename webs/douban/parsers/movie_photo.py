# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


def start_parser(text):
    data = {}
    s = BeautifulSoup(text, "lxml")
    photo_category_nodes = s.select('#content .article .mod')

    for photo_category_node in photo_category_nodes:
        photo_category_name = photo_category_node.find(
                                class_='hd'
                              ).text.strip('\n ')[:2]
        photo_nodes = photo_category_node.find_all('img')
        thumbnail_photo_urls = []
        photo_urls = []

        for photo_node in photo_nodes:
            thumbnail_photo_url = photo_node.get('src')
            thumbnail_photo_urls.append(thumbnail_photo_url)
            photo_urls.append(
                thumbnail_photo_url.replace('/albumicon', '/photo')
            )

        if photo_category_name == '剧照':
            data['photos'] = photo_urls
            data['thumbnail_photos'] = thumbnail_photo_urls
        elif photo_category_name == '海报':
            data['covers'] = photo_urls
            data['thumbnail_covers'] = thumbnail_photo_urls
        elif photo_category_name == '壁纸':
            data['wallpapers'] = photo_urls
            data['thumbnail_wallpapers'] = thumbnail_photo_urls

    return data
