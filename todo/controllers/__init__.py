# -*- coding: utf-8 -*-
# Time    : 2021/2/21 19:44
# Author  : LiaoKong
from .static import static, favicon
from .todo import index, new, delete, edit

# 注册路由
routes = {
    '/': (index, ['GET']),
    '/index': (index, ['GET']),
    '/new': (new, ['POST']),
    '/static': (static, ['GET']),
    '/favicon.ico': (favicon, ['GET']),
    '/edit': (edit, ['GET', 'POST']),
    '/delete': (delete, ['POST']),
}
