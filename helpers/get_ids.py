import models
from config import sqla; session=sqla['session']


def get_video_ids(expression=True):
    video_query = session.query(models.Video.id).filter(expression)
    return map(lambda x: x[0], video_query)

def get_celebrity_ids(expression=True):
    celebrity_query = session.query(models.Celebrity.id).filter(expression)
    return map(lambda x: x[0], celebrity_query)

def get_video_douban_ids(expression=True):
    video_query = session.query(models.Video.douban_id).filter(expression)
    return map(lambda x: x[0], video_query)

def get_celebrity_douban_ids(expression=True):
    celebrity_query = session.query(models.Celebrity.douban_id).filter(expression)
    return map(lambda x: x[0], celebrity_query)

def get_animation_bilibili_ids(expression=True):
    animation_query = session.query(models.Animation.bilibili_id).filter(expression)
    return map(lambda x: x[0], animation_query)

