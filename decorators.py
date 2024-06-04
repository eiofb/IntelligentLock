import random
from functools import wraps
from flask import g, redirect, url_for

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return inner

# 生成随机验证码
def generate_captcha():
    characters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'  # 验证码可能包含的字符
    captcha = ''.join(random.choice(characters) for _ in range(4))  # 生成4位验证码
    return captcha

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def normalize_filename(filename, name):
    return name + '.' + filename.rsplit('.', 1)[1].lower()