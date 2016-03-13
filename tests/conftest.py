import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import create_new_sqla
from helpers import (get_video_douban_ids,
                     get_celebrity_douban_ids,
                     get_animation_bilibili_ids)

test_database_url = 'sqlite:///test.db'


@pytest.fixture(scope='session')
def session(request):
    sqla = create_new_sqla(test_database_url, echo=False)

    session = sqla['session']
    engine = sqla['engine']

    Base.metadata.create_all(engine)

    def teardown():
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)

    return session


@pytest.fixture
def douban_movie_ids():
    return list(get_video_douban_ids())


@pytest.fixture
def douban_celebrity_ids():
    return list(get_celebrity_douban_ids())


@pytest.fixture
def bilibili_animation_ids():
    return list(get_animation_bilibili_ids())
