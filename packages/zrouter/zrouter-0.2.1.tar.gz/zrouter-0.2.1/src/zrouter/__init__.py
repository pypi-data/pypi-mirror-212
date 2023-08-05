from fastapi import APIRouter
from zrouter.exception import MessagePrompt
from functools import wraps
from inspirare import json


class Router(APIRouter):
    """路由"""
    def __init__(self, *args, **kwargs):
        APIRouter.__init__(self, *args, **kwargs)

    @property
    def authorized(self):
        return True

    def api_route(self, path, open=False, *args, **kwargs):
        def decorator(func):
            def func_wrapper(f):
                def wrapper(*args_, **kwargs):
                    if not (self.authorized or open):
                        return {'code': 401, 'msg': '用户无权限'}
                    try:
                        data = f(*args_, **kwargs)
                    except MessagePrompt as e:
                        return {'code': 500, 'msg': str(e)}
                    if isinstance(data, dict):
                        data = json_.iter_camel(data)
                    return {'code': 200, 'msg': '操作成功', 'data': data}
                return wrapper
            self.add_api_route(path, wraps(func)(func_wrapper(func)), *args, **kwargs)
        return decorator
    