def douban_movie_api(r):
    datas = []

    movie_base_datas = r.json().get('subjects')

    for movie_base_data in movie_base_datas:
        data = {
            'douban_id': None,
            'title': None,
            'image': None,
            'cover': None,
            'cover_x': None,
            'cover_y': None,
            'playable': None,
            'is_beetle_subject': None,
            'rate': None,
            'douban_url': None,
            'subtype': None,
            'tag': None,
            'sort': None
        }

        data['douban_id'] = movie_base_data.get('id')
        data['title'] = movie_base_data.get('title')
        data['image'] = movie_base_data.get('cover')
        data['cover'] = movie_base_data.get('cover')
        data['cover_x'] = movie_base_data.get('cover_x')
        data['cover_y'] = movie_base_data.get('cover_y')
        data['playable'] = movie_base_data.get('playable')
        data['is_beetle_subject'] = movie_base_data.get('is_beetle_subject')
        data['rate'] = movie_base_data.get('rate')
        data['douban_url'] = movie_base_data.get('url')
        
        datas.append(data)
        
    return datas
