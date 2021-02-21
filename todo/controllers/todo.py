# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:17
# Author  : LiaoKong

from todo.utils.http import redirect
from todo.utils.templating import render_template
from todo.models.todo import TodoModel


def index(request):
    """首页视图函数"""
    # 倒序排序，最近添加的 todo 排在前面
    todo_list = TodoModel.all(sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }

    return render_template('todo/index.html', **context)


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


def edit(request):
    """编辑 todo 视图函数"""
    # 处理 POST 请求
    if request.method == 'POST':
        form = request.form
        print(f'form: {form}')

        id = int(form.get('id', -1))
        content = form.get('content')

        if id != -1 and content:
            todo = TodoModel.get(id)
            if todo:
                todo.content = content
                todo.save()
        return redirect('/index')

    # 处理 GET 请求
    args = request.args
    print(f'args: {args}')

    id = int(args.get('id', -1))
    if id == -1:
        return redirect('/index')

    todo = TodoModel.get(id)
    if not todo:
        return redirect('/index')

    context = {
        'todo': todo,
    }
    return render_template('todo/edit.html', **context)


def delete(request):
    """删除 todo 视图函数"""
    form = request.form
    print(f'form: {form}')

    id = int(form.get('id', -1))
    if id != -1:
        todo = TodoModel.get(id)
        if todo:
            todo.delete()
    return redirect('/index')
