# -*- coding: utf-8 -*-
# Time    : 2021/2/21 19:58
# Author  : LiaoKong
from urllib.parse import unquote_plus


class Request(object):
    def __init__(self, request_msg):
        method, path, headers, args, form = self.parse_data(request_msg)
        self.method = method  # 请求方法 GET、POST
        self.path = path  # 请求路径 /index
        self.headers = headers  # 请求头 {'Host': '127.0.0.1:8000'}
        self.args = args  # 查询参数
        self.form = form  # 请求体

    def parse_data(self, request_msg):
        """解析请求报文"""
        header, body = request_msg.split('\r\n\r\n', 1)
        method, path, headers, args = self._parse_header(header)
        form = self._path_body(body)

        return method, path, headers, args, form

    def _parse_header(self, header_data):
        request_line, request_header = header_data.split('\r\n', 1)

        # 请求行拆包 'GET /index HTTP/1.1' -> ['GET', '/index', 'HTTP/1.1']
        method, path_query, _ = request_line.split()
        path, args = self._parse_path(path_query)

        headers = {}
        for header in request_header.split('\r\n'):
            k, v = header.split(': ', 1)
            headers[k] = v

        return method, path, headers, args

    @staticmethod
    def _parse_path(data):
        """解析请求路径、请求参数"""
        args = {}
        # 请求路径和 GET 请求参数格式: /index?edit=1&content=text
        if '?' not in data:
            path, query = data, ''
        else:
            path, query = data.split('?', 1)
            for q in query.split('&'):
                k, v = q.split('=', 1)
                args[k] = v
        return path, args

    @staticmethod
    def _path_body(data):
        """解析请求体"""
        form = {}
        if data:
            # POST 请求体参数格式: username=zhangsan&password=mima
            for b in data.split('&'):
                k, v = b.split('=', 1)
                # 前端页面中通过 form 表单提交过来的数据会被自动编码，使用 unquote_plus 来解码
                form[k] = unquote_plus(v)
        return form


class Response(object):
    response_msg_by_code = {
        200: 'OK',
        302: 'FOUND',
        405: 'METHOD NOT ALLOWED',
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
        header += ''.join(f'{k}: {v}\r\n' for k, v in self.headers.items())

        # 空行
        blank_line = '\r\n'

        # 响应体
        body = self.body

        # body 支持 str 或 bytes 类型
        if isinstance(body, str):
            body = body.encode('utf-8')
        response_msg = (header + blank_line).encode('utf-8') + body
        return response_msg


def redirect(url, status=302):
    """重定向"""
    headers = {
        'Location': url,
    }
    body = ''
    return Response(body, headers=headers, status=status)
