from webs import pq


def get_douban_movie_data(r):
    data = {
        'title':'',
    }
    if r.status_code != 404:
        d = pq(r.text)
        data['title'] = d('#content h1 span').text()
    else:
        data = None

    return data
