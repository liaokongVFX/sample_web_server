# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:01
# Author  : LiaoKong
import os

from todo.config import BASE_DIR


def render_template(template_path):
    """读取Html内容"""
    template_dir = os.path.join(BASE_DIR, 'templates')
    path = os.path.join(template_dir, template_path)
    with open(path, encoding='utf-8') as f:
        return f.read()


class Request(object):
    def __init__(self, request_msg):
        self.method, self.path, self.headers = self.parse_data(request_msg)

    def parse_data(self, request_msg):
        """解析请求报文"""
        header, body = request_msg.split('\r\n\r\n', 1)
        method, path, headers = self._parse_header(header)
        return method, path, headers

    @staticmethod
    def _parse_header(header_data):
        request_line, request_header = header_data.split('\r\n', 1)

        #  request_line: 'GET /index HTTP/1.1'
        method, path, _ = request_line.split()

        headers = {}
        for header in request_header.split('\r\n'):
            k, v = header.split(': ', 1)
            headers[k] = v

        return method, path, headers


class Response(object):
    response_msg_by_code = {
        200: 'OK',
        405: 'METHOD NOT ALLOWED'
    }

    def __init__(self, body, headers=None, status=200):
        # 默认响应首部字段，指定响应内容的类型为 HTML
        _headers = {
            'Content-Type': 'text/html; charset=utf-8',
        }
        if headers:
            _headers.update(headers)

        self.headers = _headers
        self.body = body
        self.status = status

    def __bytes__(self):
        """构造响应报文"""
        # 状态行 'HTTP/1.1 200 OK\r\n'
        header = f'HTTP/1.1 {self.status} {self.response_msg_by_code.get(self.status, "")}\r\n'

        # 响应头部
        header += ''.join(f'{k}: {v}' for k, v in self.headers.items())

        # 空行
        blank_line = '\r\n\r\n'

        # 响应体
        body = self.body

        response_msg = header + blank_line + body
        print(response_msg)
        return response_msg.encode('utf-8')
