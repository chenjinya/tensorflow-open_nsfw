
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import urllib
import json
import time
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get(url, param):
    url = url + "?" + urllib.parse.urlencode(param)
    print("Get url:", url)
    resu = urllib.request.urlopen(
        url, None, timeout=10)
    data = resu.read().decode()
    return data


def post(url, param):
    # 设置请求头 告诉服务器请求携带的是json格式的数据
    headers = {'Content-Type': 'application/json'}
    request = urllib.request.Request(url=url, headers=headers, data=json.dumps(
        param).encode(encoding='UTF8'))  # 需要通过encode设置编码 要不会报错
    response = urllib.request.urlopen(request)  # 发送请求
    data = response.read().decode()  # 读取对象 将返回的二进制数据转成string类型
    return data


def download(remote_path, dir_path):
    def downloading(a, b, c):
        per = 100.0*a*b/c
        if per > 100:
            per = 100
            print('%.2f%%' % per)
        else:
            print('=', end='')

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        arr = os.path.split(remote_path)
        file_name = arr[1]
        file_path = '{}{}{}'.format(dir_path, os.sep, file_name)
        urllib.request.urlretrieve(remote_path, file_path, downloading)
        return file_path
    except IOError as e:
        print("IOError", e)
    except Exception as e:
        print(e, sys._getframe().f_lineno)
