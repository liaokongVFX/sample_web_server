# -*- coding: utf-8 -*-
# Time    : 2021/2/14 21:49
# Author  : LiaoKong
import socket
import threading

from todo.config import HOST, POST, BUFFER_SIZE
from todo.utils import Request, Response
from todo.controllers import routes


def make_response(request, headers=None):
    """构造响应报文"""
    # 默认状态码为 200
    status = 200

    # 获取匹配当前请求路径的处理函数和函数所接收的请求方法
    # request.path 等于 '/' 或 '/index' 时，routes.get(request.path) 将返回 (index, ['GET'])
    route, methods = routes.get(request.path)
    if request.method not in methods:
        status = 405
        data = 'Method Not Allowed'
    else:
        data = route()

    # 获取响应报文
    response = Response(data, headers=headers, status=status)
    response_bytes = bytes(response)
    print(f'response_bytes: {response_bytes}')

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
    print(f'request_message: {request_msg}')

    # 解析请求
    request = Request(request_msg)
    # 根据请求对象构造响应报文
    response_bytes = make_response(request)
    # 返回响应
    client.sendall(response_bytes)

    client.close()


def main():
    with socket.socket() as s:
        # 允许端口复用
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, POST))
        s.listen(5)
        print(f'running on http://{HOST}:{POST}')

        while 1:
            client, address = s.accept()
            print(f'client address: {address}')

            # 创建一条子线程去处理客户端请求
            t = threading.Thread(target=process_connection, args=(client,))
            t.start()


if __name__ == '__main__':
    main()
