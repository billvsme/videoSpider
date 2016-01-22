#!/usr/bin/env python3
import os
import time
import sys
from gevent import monkey;
monkey.patch_socket()
monkey.patch_os()
from webs import douban


if __name__ == '__main__':
    start = time.time()

    if len(sys.argv)  == 1:
        os.system('python start.py full')
    elif sys.argv[1] == 'base':
        douban.works.get_main_movies_base_data.start_work()

        end = time.time()
        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'movie':
        douban.works.get_main_movies_full_data.start_work(process_number=2)

        end = time.time()
        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'celebrity':
        douban.works.get_celebrities_full_data.start_work(process_number=2)

    elif sys.argv[1] == 'full':
        os.system('python start.py base')
        os.system('python start.py movie')
        os.system('python start.py celebrity')
        end = time.time()
        print('use {}s'.format(end-start))

    elif sys.argv[1] == 'test':
        douban.works.get_main_movies_full_data.start_work()
        douban.works.get_celebrities_full_data.start_work()
        end = time.time()
        print('use {}s'.format(end-start))
