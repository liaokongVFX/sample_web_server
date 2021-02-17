# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:17
# Author  : LiaoKong

from todo.utils import render_template
from todo.models import TodoModel


def index():
    """首页视图函数"""
    # 倒序排序，最近添加的 todo 排在前面
    todo_list = TodoModel.all(sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }

    return render_template('index.html', **context)


# 注册路由
routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
}
