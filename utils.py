# coding=utf-8
""" Utility functions """
import pwd
import grp
from bottle import request, abort

def get_used_percent(quota, used):
    return (used*100.0)/max(quota,used+0.01)

def get_available_percent(quota, used):
    return (quota*100.0)/max(quota,used+0.01)

def getcurrentuser():
    result = ""
    if "REMOTE_USER" in request.environ:
        result = request.environ["REMOTE_USER"]
    return result

def normaliseuser(user):
    user = user.split('@')[0]
    return user

def get_users_groups(user):
    passwd = None
    try:
        passwd = pwd.getpwnam(normaliseuser(user))
    except KeyError:
        return set()
    groups = []
    groups.append(grp.getgrgid(passwd[3])[0])
    for i in grp.getgrall():
        if user in i[3]:
            groups.append(i[0])
    return set(groups)

def is_in_groups(user, groups):
    usergroups = get_users_groups(user)
    return any((i in usergroups) for i in groups)

def is_a_user(user, users):
    return any(normaliseuser(user) == normaliseuser(i) for i in users)

def require_users(users):
    def decorator_require_users(func):
        def wrap_require_users(*args,**kwargs):
            value = func(*args, **kwargs)
            if is_a_user(getcurrentuser(), users):
                return value
            abort(403, "Unauthorised")
        return wrap_require_users
    return decorator_require_users

def require_user(user):
    def decorator_require_user(func):
        def wrap_require_user(*args,**kwargs):
            value = func(*args, **kwargs)
            if is_a_user(getcurrentuser(), [user,]):
                return value
            abort(403, "Unauthorised")
        return wrap_require_user
    return decorator_require_user


def require_group(group):
    def decorator_require_group(func):
        def wrap_require_group(*args,**kwargs):
            value = func(*args, **kwargs)
            if is_in_groups(normaliseuser(getcurrentuser()), [group,]):
                return value
            abort(403, "Unauthorised")
        return wrap_require_group
    return decorator_require_group

def require_groups(groups):
    def decorator_require_groups(func):
        def wrap_require_groups(*args,**kwargs):
            value = func(*args, **kwargs)
            if is_in_groups(normaliseuser(getcurrentuser()), groups):
                return value
            abort(403, "Unauthorised")
        return wrap_require_groups
    return decorator_require_groups
