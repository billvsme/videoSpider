import re
from bs4 import BeautifulSoup


def get_celebrity_info(node):
    celebrity_nodes = node.next_sibling.next_sibling.find_all('a')
    celebrities = [
        {
            'name': celebrity.string,
            'douban_url': celebrity['href'],
            'douban_id': re.findall(r'\d+', celebrity['href'])[0] if re.match(r'/celebrity/\d+/',celebrity['href']) else None
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
        types = []
        node = node_dict['类型']
        while(node.name != 'br'):
            if node.name == 'span':
                types.append(node.string)
            node = node.next_sibling

        movie_info['types'] = types

    if '官方网站' in node_dict:
        movie_info['official_site'] = node_dict['官方网站'].next_sibling.next_sibling.get('href')

    if '制片国家/地区' in node_dict:
        movie_info['countries'] = [
            name.strip() for name in node_dict['制片国家/地区'].next_sibling.string.split('/')
        ]

    if '上映日期' in node_dict:
        movie_info['pubdate'] = node_dict['上映日期'].next_sibling.next_sibling.string

    if '片长' in node_dict:
        movie_info['duration'] = node_dict['片长'].next_sibling.next_sibling.string

    if '又名' in node_dict:
        movie_info['aliases'] = [
            name.strip() for name in node_dict['又名'].next_sibling.string.split('/')
        ]

    if 'IMDb链接' in node_dict:
        movie_info['imdb_number'] = node_dict['IMDb链接'].next_sibling.next_sibling.string

    return movie_info


def douban_movie_page(r):
    data = {
        'title': '',
    }
    if r.status_code != 404:
        s = BeautifulSoup(r.text, "lxml")

        data['douban_url'] = r.url
        data['title'] = s.select('#content h1 span')[0].string
        data['genres'] = [x.string for x in s.find(id='info').find_all(property='v:genre')]
        data['summary'] = s.find(property='v:summary').string if s.find(property='v:summary') != None else None

        class_pl_dict = {}
        class_pl_nodes = s.select('.pl')
        for node in class_pl_nodes:
            dict_key = node.string
            if dict_key is not None:
                dict_key = dict_key[:-1] if dict_key.endswith(':') else dict_key
                class_pl_dict[dict_key] = node

        data.update(get_movie_info(class_pl_dict))
        data['douban_rate'] = s.select('.rating_num')[0].string

    else:
        data = None

    return data
