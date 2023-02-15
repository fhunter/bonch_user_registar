# coding=utf-8
""" Utility functions """
from bottle import request


def getcurrentuser():
    result = ""
    if "REMOTE_USER" in request.environ:
        result = request.environ["REMOTE_USER"]
    return result

def normaliseuser(user):
    user = user.split('@')[0]
    return user
