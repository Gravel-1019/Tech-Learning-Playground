"""
公共方法
"""

import logging.config
from conf import settings


# 登录认证装饰器
def login_auth(func):
    def wrapper(*args, **kwargs):
        from core import src
        if src.logged_user:
            res = func(*args, **kwargs)
            return res
        else:
            print('\n你个憨憨，还没有登录呢！')
            src.login()
    return wrapper


# 密码加密
def pwd_to_sha256(password):
    import hashlib
    sha = hashlib.sha256()
    sha.update(password.encode('utf-8'))
    sha.update('接着奏乐接着舞'.encode('utf-8-sig'))
    return sha.hexdigest()


# 日志记录功能
def get_logger(logger_name):
    # 1、加载日志配置字典
    logging.config.dictConfig(settings.LOGGING_DIC)

    # 2、获取logger
    logger = logging.getLogger(logger_name)
    return logger
