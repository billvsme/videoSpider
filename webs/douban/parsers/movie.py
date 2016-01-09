from webs import pq


def douban_movie_page(r):
    data = {
        'title':'',
    }
    if r.status_code != 404:
        d = pq(r.text)
        data['title'] = d('#content h1 span').text()
    else:
        data = None

    return data
