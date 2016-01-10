#!/usr/bin/env python3
from webs import douban

from gevent import monkey
monkey.patch_socket()


douban.works.get_main_movies_full_data.start()
