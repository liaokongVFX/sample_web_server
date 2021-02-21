# -*- coding: utf-8 -*-
# Time    : 2021/2/17 20:19
# Author  : LiaoKong

from . import Model


class TodoModel(Model):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.user_id = kwargs.get('user_id', -1)
        self.content = kwargs.get('content', '')
