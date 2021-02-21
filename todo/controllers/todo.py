# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:17
# Author  : LiaoKong

from todo.utils.http import redirect
from todo.utils.templating import render_template
from todo.models.todo import TodoModel
from todo.utils.logging import logger
from todo.controllers.auth import current_user
from todo.utils.auth import login_required


@login_required
def index(request):
    """首页视图函数"""
    # 倒序排序，最近添加的 todo 排在前面
    user = current_user(request)
    todo_list = TodoModel.find_by(user_id=user.id, sort=True, reverse=True)
    context = {
        'todo_list': todo_list,
    }

    return render_template('todo/index.html', **context)


@login_required
def new(request):
    """新建 todo 视图函数"""
    form = request.form
    logger(f'form: {form}')

    content = form.get('content')
    # 这里判断前端传递过来的参数是否有内容，如果为空则说明不是一个有效的 todo，直接重定向到首页
    if content:
        user = current_user(request)
        if user:
            todo = TodoModel(content=content, user_id=user.id)
            todo.save()
    return redirect('/index')


@login_required
def edit(request):
    """编辑 todo 视图函数"""
    # 处理 POST 请求
    if request.method == 'POST':
        form = request.form
        logger(f'form: {form}')

        id = int(form.get('id', -1))
        content = form.get('content')

        if id != -1 and content:
            user = current_user(request)
            if user:
                todo = TodoModel.find_by(id=id, user_id=user.id, ensure_one=True)
                if todo:
                    todo.content = content
                    todo.save()
        return redirect('/index')

    # 处理 GET 请求
    args = request.args
    logger(f'args: {args}')

    id = int(args.get('id', -1))
    if id == -1:
        return redirect('/index')

    user = current_user(request)
    if not user:
        return redirect('/index')

    todo = TodoModel.find_by(id=id, user_id=user.id, ensure_one=True)
    if not todo:
        return redirect('/index')

    context = {
        'todo': todo,
    }
    return render_template('todo/edit.html', **context)


@login_required
def delete(request):
    """删除 todo 视图函数"""
    form = request.form
    logger(f'form: {form}')

    id = int(form.get('id', -1))
    if id != -1:
        user = current_user(request)
        if user:
            todo = TodoModel.find_by(id=id, user_id=user.id, ensure_one=True)
            if todo:
                todo.delete()

    return redirect('/index')
