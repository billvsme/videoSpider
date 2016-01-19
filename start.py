#!/usr/bin/env python3
import time
from webs import douban

from gevent import monkey
monkey.patch_socket()


start = time.time()

douban.works.get_main_movies_full_data.start_work()

end = time.time()

print('use %s', end-start)

