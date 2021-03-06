# -*- coding: utf-8 -*-
# Time    : 2021/2/14 21:49
# Author  : LiaoKong
import socket
import threading

from todo.config import HOST, POST, BUFFER_SIZE
from todo.utils.http import Request, Response
from todo.controllers import routes
from todo.utils.logging import logger
from todo.utils.error import errors


def make_response(request, headers=None):
    """构造响应报文"""
    # 默认状态码为 200
    status = 200

    # 处理静态资源请求
    if request.path.startswith('/static'):
        route, methods = routes.get('/static')
    else:
        try:
            # 获取匹配当前请求路径的处理函数和函数所接收的请求方法
            # request.path 等于 '/' 或 '/index' 时，routes.get(request.path) 将返回 (index, ['GET'])
            route, methods = routes.get(request.path)
        except TypeError:
            # 返回给用户 404 页面
            return bytes(errors[404]())

    if request.method not in methods:
        status = 405
        data = 'Method Not Allowed'
    else:
        data = route(request)

    # 如果返回结果为 Response 对象，直接获取响应报文
    if isinstance(data, Response):
        response_bytes = bytes(data)
    else:
        # 返回结果为字符串，需要先构造 Response 对象，然后再获取响应报文
        response = Response(data, headers=headers, status=status)
        response_bytes = bytes(response)

    logger(f'response_bytes: {response_bytes}')
    return response_bytes


def process_connection(client):
    # 处理客户端过来的请求
    request_bytes = b''
    while 1:
        chunk = client.recv(BUFFER_SIZE)
        request_bytes += chunk
        if len(chunk) < BUFFER_SIZE:
            break

    # 请求报文
    request_msg = request_bytes.decode('utf-8')
    logger(f'request_message: {request_msg}')

    # 解析请求
    request = Request(request_msg)
    try:
        # 根据请求报文构造响应报文
        response_bytes = make_response(request)
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger(e)
        # 返回给用户 500 页面
        response_bytes = bytes(errors[500]())
    # 返回响应
    client.sendall(response_bytes)

    client.close()


def main():
    with socket.socket() as s:
        # 允许端口复用
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, POST))
        s.listen(5)
        logger(f'running on http://{HOST}:{POST}')

        while 1:
            client, address = s.accept()
            logger(f'client address: {address}')

            # 创建一条子线程去处理客户端请求
            t = threading.Thread(target=process_connection, args=(client,))
            t.start()


if __name__ == '__main__':
    main()
