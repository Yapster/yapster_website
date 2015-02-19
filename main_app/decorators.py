from functools import wraps
from django.shortcuts import redirect


def user_has_perm(view_function):
    def _decorator(request, *args, **kwargs):
        try:
            request.COOKIES['u']
            request.COOKIES['s']
            response = view_function(request, *args, **kwargs)
        except KeyError:
            response = redirect('/')
        return response
    return wraps(view_function)(_decorator)