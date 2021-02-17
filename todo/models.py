# -*- coding: utf-8 -*-
# Time    : 2021/2/17 20:19
# Author  : LiaoKong

import os
import json

from todo.config import BASE_DIR


class TodoModel(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.content = kwargs.get('content', '')

    @classmethod
    def _db_path(cls):
        return os.path.join(BASE_DIR, 'db/todo.json')

    @classmethod
    def _load_db(cls):
        path = cls._db_path()
        with open(path, encoding='utf-8') as f:
            return json.load(f)

    @classmethod
    def all(cls, sort=False, reverse=False):
        todo_list = [cls(**todo_dict) for todo_dict in cls._load_db()]
        if sort:
            todo_list = sorted(todo_list, key=lambda x: x.id, reverse=reverse)
        return todo_list
