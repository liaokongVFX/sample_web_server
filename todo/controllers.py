# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:17
# Author  : LiaoKong
import os

from todo.config import BASE_DIR
from todo.utils import render_template, Response, redirect
from todo.models import TodoModel


def index(request):
    """首页视图函数"""
    # 倒序排序，最近添加的 todo 排在前面
    todo_list = TodoModel.all(sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }

    return render_template('index.html', **context)


def static(request):
    """读取静态资源视图函数"""
    # 能够处理的静态资源类型
    content_type = {
        'css': 'text/css',
        '.js': 'text/javascript',
        'png': 'image/png',  # 文件需要返回二进制
        'jpg': 'image/jpeg',
    }
    # 请求路径格式：/static/css/style.css
    # 根据请求路径中的文件名后缀判断静态文件类型，指定响应首部字段 Content-Type
    headers = {
        'Content-Type': content_type.get(request.path[-3:], 'text/plain'),
    }

    # 获取静态资源绝对路径
    path = request.path.lstrip('/')
    file_path = os.path.join(BASE_DIR, path)

    # 读取静态资源内容，构造响应对象并返回
    with open(file_path) as f:
        body = f.read()
    return Response(body, headers=headers)


def favicon(request):
    """读取网页 ICO 图标"""
    headers = {
        'Content-Type': 'image/x-icon',
    }
    path = f'static/{request.path.lstrip("/")}'
    file_path = os.path.join(BASE_DIR, path)
    # ICO 图标文件需要读取为二进制
    with open(file_path, 'rb') as f:
        body = f.read()
    return Response(body, headers=headers)


def new(request):
    """新建 todo 视图函数"""
    form = request.form
    print(f'form: {form}')

    content = form.get('content')
    # 这里判断前端传递过来的参数是否有内容，如果为空则说明不是一个有效的 todo，直接重定向到首页
    if content:
        todo = TodoModel(content=content)
        todo.save()
    return redirect('/index')


# 注册路由
routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
    '/new': (new, ['POST']),
    '/static': (static, ['GET']),
    '/favicon.ico': (favicon, ['GET']),
}
