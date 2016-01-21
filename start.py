#!/usr/bin/env python3
import os
import time
import sys
from gevent import monkey; monkey.patch_socket()
from webs import douban


if __name__ == '__main__':

    start = time.time()
    if sys.argv[1] == 'base':
        douban.works.get_main_movies_base_data.start_work()

    if sys.argv[1] == 'movie':
        douban.works.get_main_movies_full_data.start_work()

    if sys.argv[1] == 'celebrity':
        douban.works.get_celebrities_full_data.start_work()

    if sys.argv[1] == 'full':
        os.system('python start.py base')
        end = time.time()
        print('use {}s'.format(end-start))
        os.system('python start.py movie')
        end = time.time()
        print('use {}s'.format(end-start))
        os.system('python start.py celebrity')
        end = time.time()
        print('use {}s'.format(end-start))

    if len(sys.argv)  == 1:
        os.system('python start.py full')
