# -*- coding: utf-8 -*-
# Time    : 2021/2/21 21:18
# Author  : LiaoKong
import functools

from todo.controllers.auth import current_user
from todo.utils.http import redirect


def login_required(func):
    """验证登录装饰器"""

    @functools.wraps(func)
    def wrapper(request):
        user = current_user(request)
        if not user:
            return redirect('/login')
        result = func(request)
        return result

    return wrapper
