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
    def _save_db(cls, data):
        path = cls._db_path()
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    @classmethod
    def all(cls, sort=False, reverse=False):
        todo_list = [cls(**todo_dict) for todo_dict in cls._load_db()]
        if sort:
            todo_list = sorted(todo_list, key=lambda x: x.id, reverse=reverse)
        return todo_list

    def save(self):
        # 查找出除 self 以外所有 todo
        # todo.__dict__ 是保存了所有实例属性的字典
        todo_list = [todo.__dict__ for todo in self.all(sort=True) if todo.id != self.id]

        # 自增 id
        if self.id is None:
            # 如果 todo_list 长度大于 0 说明不是第一条 todo，取最后一条 todo 的 id 加 1
            if len(todo_list) > 0:
                self.id = todo_list[-1]['id'] + 1
            # 否则说明是第一条 todo，id 为 1
            else:
                self.id = 1

        # 将当前 todo 追加到 todo_list
        todo_list.append(self.__dict__)
        # 将所有 todo 保存到文件
        self._save_db(todo_list)

    @classmethod
    def find_by(cls, limit=-1, ensure_one=False, sort=False, reverse=False, **kwargs):
        """查询 todo"""
        result = []
        todo_list = [todo.__dict__ for todo in cls.all(sort=sort, reverse=reverse)]
        for todo in todo_list:
            # 根据关键字参数查询 todo
            for k, v in kwargs.items():
                if todo.get(k) != v:
                    break
            else:
                result.append(cls(**todo))

        # 查询给定条数的数据
        if 0 < limit < len(result):
            result = result[:limit]
        # 查询结果集中的第一条数据
        if ensure_one:
            result = result[0] if len(result) > 0 else None

        return result

    @classmethod
    def get(cls, id):
        """通过 id 查询 todo"""
        result = cls.find_by(id=id, ensure_one=True)
        return result

    def delete(self):
        """删除 todo"""
        todo_list = [todo.__dict__ for todo in self.all() if todo.id != self.id]
        self._save_db(todo_list)

