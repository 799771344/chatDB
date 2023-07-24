import os
import socket
import threading
import json
import random
from urllib.parse import urlencode


async def singleton(cls):
    instances = {}
    lock = threading.Lock()

    async def _singleton(*args, **kwargs):
        with lock:
            if cls not in instances:
                instances[cls] = await cls(*args, **kwargs)
        return instances[cls]

    return _singleton


# 获取本地IP地址
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip
