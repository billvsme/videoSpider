# -*- coding: utf-8 -*-
import random
import string


def random_str(randomlength=8):
    a = list(string.ascii_letters+'0123456789')
    random.shuffle(a)
    return ''.join(a[:randomlength])
