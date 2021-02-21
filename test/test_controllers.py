# -*- coding: utf-8 -*-
# Time    : 2021/2/21 20:12
# Author  : LiaoKong

import os
import sys
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo.utils.http import Request
from todo.controllers import routes
from todo.models.todo import TodoModel


def test_index():
    """测试首页"""
    request_message = 'GET / HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\n'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)

    assert b'Todo List' in bytes(r, encoding='utf-8')
    assert b'/new' in bytes(r, encoding='utf-8')


def test_new():
    """测试新增 todo"""
    # 生成随机 todo 内容
    content = uuid.uuid4().hex
    request_message = f'POST /new HTTP/1.1\r\nHost: 127.0.0.1:8000\r\n\r\ncontent={content}'
    request = Request(request_message)
    route, method = routes.get(request.path)
    r = route(request)
    t = TodoModel.find_by(content=content, ensure_one=True)
    t.delete()

    assert b'302 FOUND' in bytes(r)
    assert b'/index' in bytes(r)
    assert t.content == content


def main():
    test_index()
    test_new()


if __name__ == '__main__':
    main()
