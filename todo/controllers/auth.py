# -*- coding: utf-8 -*-
# Time    : 2021/2/21 20:45
# Author  : LiaoKong

from todo.models.user import User
from todo.utils.logging import logger
from todo.utils.http import redirect
from todo.utils.templating import render_template
from todo.models.session import Session


def register(request):
    """注册视图函数"""
    if request.method == 'POST':
        # 获取表单中的用户名和密码
        form = request.form
        logger(f'form: {form}')
        username = form.get('username')
        raw_password = form.get('password')

        # 验证用户名和密码是否合法
        if not username or not raw_password:
            return '无效的用户名或密码'.encode('utf-8')
        user = User.find_by(username=username, ensure_one=True)
        if user:
            return '用户名已存在'.encode('utf-8')

        # 对密码进行散列计算，创建并保存用户信息
        password = User.generate_password(raw_password)
        user = User(username=username, password=password)
        user.save()
        # 注册成功后重定向到登录页面
        return redirect('/login')

    return render_template('auth/register.html')


def current_user(request):
    """获取当前登录用户"""
    # 从 Cookie 中获取 session_id
    cookies = request.cookies
    logger(f'cookies: {cookies}')
    session_id = cookies.get('session_id')

    # 查找 Session 并验证其是否过期
    session = Session.get(session_id)
    if not session:
        return None
    if session.is_expired():
        session.delete()
        return None

    # 查找当前登录用户
    user = User.get(session.user_id)
    if not user:
        return None
    return user


def login(request):
    """登录视图函数"""
    # 如果用户已经登录，直接重定向到首页
    if current_user(request):
        return redirect('/index')

    if request.method == 'POST':
        message = '用户名或密码不正确'.encode('utf-8')

        # 获取表单中的用户名和密码
        form = request.form
        logger(f'form: {form}')
        username = form.get('username')
        raw_password = form.get('password')

        # 验证用户名和密码是否正确
        if not username or not raw_password:
            return message
        user = User.find_by(username=username, ensure_one=True)
        if not user:
            return message
        password = user.password
        if not User.validate_password(raw_password, password):
            return message

        # 创建 Session 并将 session_id 写入 Cookie 实现登录
        session = Session(user_id=user.id)
        session.save()
        cookies = {
            'session_id': session.id,
        }
        return redirect('/index', cookies=cookies)

    return render_template('auth/login.html')
