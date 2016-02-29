# -*- coding: utf-8 -*-
import functools
from tqdm import tqdm


class progress(object):
    def __init__(self, start_info=None, end_info=None, desc=None):
        self.start_info = start_info
        self.end_info = end_info
        self.desc = desc

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self.start_info is not None:
                print(self.start_info)
            async_result = func()
            if async_result is not None:
                self.print_progress(async_result, self.desc)
            if self.end_info is not None:
                print(self.end_info)

        return wrapper

    def print_progress(self, async_result, desc):
        pbar = tqdm(total=len(async_result), desc=desc)
        completed_count = 0
        while(completed_count != len(async_result)):
            update_completed_count = async_result.completed_count()
            updata_count = update_completed_count - completed_count
            if updata_count != 0:
                pbar.update(updata_count)
            completed_count = update_completed_count
