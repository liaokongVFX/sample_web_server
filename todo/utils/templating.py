# -*- coding: utf-8 -*-
# Time    : 2021/2/14 22:01
# Author  : LiaoKong
import os
import re

from todo.config import BASE_DIR


class Template(object):
    def __init__(self, text, context):
        # 保存最终结果
        self.result = []
        # 保存从 HTML 中解析出来的 for 语句代码片段
        self.for_snippet = []
        # 上下文变量
        self.context = context
        # 使用正则匹配出所有的 for 语句、模板变量
        self.snippets = re.split('({{.*?}}|{%.*?%})', text, flags=re.DOTALL)
        # 标记是否为 for 语句代码段
        is_for_snippet = False

        for snippet in self.snippets:
            # 解析模板变量
            if snippet.startswith('{{'):
                if not is_for_snippet:
                    var = snippet[2:-2].strip()
                    snippet = self._get_var_value(var)
            # 解析 for 语句
            elif snippet.startswith('{%'):
                # for 语句开始代码片段 -> {% for todo in todo_list %}
                if 'in' in snippet:
                    is_for_snippet = True
                    self.result.append('{}')
                    # for 语句结束代码片段 -> {% endfor %}
                else:
                    is_for_snippet = False
                    snippet = ''

            if is_for_snippet:
                # 如果是 for 语句代码段，需要进行二次处理，暂时保存到 for 语句片段列表中
                self.for_snippet.append(snippet)
            else:
                # 如果是模板变量，直接将变量值追加到结果列表中
                self.result.append(snippet)

    def _get_var_value(self, var):
        """根据变量名获取变量的值"""
        # 如果 '.' 不在变量名中，直接在上下文变量中获取变量的值
        if '.' not in var:
            value = self.context.get(var)
            # '.' 在变量名中（对象.属性），说明是要获取对象的属性
        else:
            obj, attr = var.split('.')
            value = getattr(self.context.get(obj), attr)
        # 保证返回的变量值为字符串
        if not isinstance(value, str):
            value = str(value)
        return value

    def _parse_for_snippet(self):
        """解析 for 语句片段代码"""
        # 保存 for 语句片段解析结果
        result = []
        if self.for_snippet:
            # 解析 for 语句开始代码片段
            # '{% for todo in todo_list %}' -> ['for', 'todo', 'in', 'todo_list']
            words = self.for_snippet[0][2:-2].strip().split()
            # 从上下文变量中获取 for 语句中的可迭代对象
            iter_obj = self.context.get(words[-1])

            for i in iter_obj:
                # 遍历 for 语句片段的代码块
                for snippet in self.for_snippet[1:]:
                    # 解析模板变量
                    if snippet.startswith('{{'):
                        # 去掉花括号和空格，获取变量名
                        var = snippet[2:-2].strip()
                        # 如果 '.' 不在变量名中，直接将循环变量 i 赋值给 snippet
                        if '.' not in var:
                            snippet = i
                        # '.' 在变量名中（对象.属性），说明是要获取对象的属性
                        else:
                            obj, attr = var.split('.')
                            # 将对象的属性值赋值给 snippet
                            snippet = getattr(i, attr)
                    # 保证变量值为字符串
                    if not isinstance(snippet, str):
                        snippet = str(snippet)
                    # 将解析出来的循环变量结果追加到 for 语句片段解析结果列表中
                    result.append(snippet)
        return result

    def render(self):
        """渲染"""
        # 获取 for 语句片段解析结果
        for_result = self._parse_for_snippet()
        # 将渲染结果组装成字符串并返回
        return ''.join(self.result).format(''.join(for_result))


def render_template(template_path, **context):
    """渲染模板"""
    template_dir = os.path.join(BASE_DIR, 'templates')
    path = os.path.join(template_dir, template_path)
    with open(path, encoding='utf-8') as f:
        t = Template(f.read(), context)

    return t.render()
