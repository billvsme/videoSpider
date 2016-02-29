# -*- coding: utf-8 -*-
import os
import requests


def down(url, cookies, path, filename):
    r = requests.get(url, cookies=cookies, timeout=10)
    try:
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(r.content)
    except FileNotFoundError:
        os.makedirs(path)
        with open(os.path.join(path, filename), 'wb') as f:
            f.write(r.content)
