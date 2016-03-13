import pytest
import webs
import models
from gevent import monkey
monkey.patch_socket()


class TestVideoSpider():
    def test_entry_points(self):
        webs.douban.parsers.movie
        webs.douban.parsers.celebrity
        webs.douban.parsers.douban_api
        webs.douban.parsers.movie_photo
        webs.douban.tasks.get_main_movies_base_data
        webs.douban.tasks.get_main_movies_full_data
        webs.douban.tasks.get_celebrities_full_data
        webs.douban.tasks.down_video_images
        webs.douban.tasks.down_celebrity_images

        webs.bilibili.parsers.bilibili_api
        webs.bilibili.parsers.animation
        webs.bilibili.tasks.get_animations_base_data
        webs.bilibili.tasks.get_animations_full_data

    def test_douban_movie_base_data(self, session):
        douban_movie_ids = webs.douban.tasks.get_main_movies_base_data.task(
            20,
            types=['movie'],
            sorts=['recommend'],
            tags_dict={
                'movie': ['热门']
            }
        )

    def test_douban_movie_full_data(self, session, douban_movie_ids):
        webs.douban.tasks.get_main_movies_full_data.task(
            douban_movie_ids[:10],
            5
        )

        videos = session.query(models.Video).filter_by(is_detail=True).all()

        assert len(videos) == 10

    def test_douban_celebrity_full_data(self, session, douban_celebrity_ids):
        webs.douban.tasks.get_celebrities_full_data.task(
            douban_celebrity_ids[:10],
            5
        )

        celebrities = session.query(
            models.Celebrity
        ).filter_by(is_detail=True).all()

        assert len(celebrities) == 10

    def test_bilibili_animation_base_data(self, session):
        webs.bilibili.tasks.get_animations_base_data.task(20, [1])

    def test_bilibili_animation_full_data(self,
                                          session,
                                          bilibili_animation_ids):
        webs.bilibili.tasks.get_animations_full_data.task(
            bilibili_animation_ids[:10],
            5
        )

        animations = session.query(
            models.Animation
        ).filter_by(is_detail=True).all()

        assert len(animations) == 10
