import models
from config import sqla; session=sqla['session']


def get_video_douban_ids(expression=True):
    video_douban_ids = set()
    video_query = session.query(models.Video.douban_id).filter(expression)
    for douban_id, in video_query:
        video_douban_ids.add(douban_id)

    return video_douban_ids

def get_celebrity_douban_ids(expression=True):
    celebrity_douban_ids = set()
    celebrity_query = session.query(models.Celebrity.douban_id).filter(expression)
    for douban_id, in celebrity_query:
        celebrity_douban_ids.add(douban_id)

    return celebrity_douban_ids

def get_animation_bilibili_ids(expression=True):
    animation_bilibili_ids = set()
    animation_query = session.query(models.Animation.bilibili_id).filter(expression)
    for bilibili_id, in animation_query:
        animation_bilibili_ids.add(bilibili_id)
    
    return animation_bilibili_ids

