import pytest
import webs


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
