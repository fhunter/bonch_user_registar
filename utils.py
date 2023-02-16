# coding=utf-8
""" Utility functions """
from bottle import request

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
