# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:17
# Author  : LiaoKong

from todo.utils import render_template


def index():
    """首页视图函数"""
    return render_template('index.html')


# 注册路由
routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
}
