"""
用户相关接口
"""
from db import  db_handler
from lib import common


logger = common.get_logger('user')
#注册接口
def register_interface(username,password,is_admin = False,balance=0):
    '''
    注册接口
    :param username: 用户名 str
    :param password: 密码  str
    :param is_admin: 是否位admin bool
    :param balance: 余额 int
    :return:(bool str)
    '''

    if db_handler.select_data(username, False):
        return False, '\n用户名已存在！'


    user_data = {
        'username': username,
        'password': password,
        'balance': balance,
        'shopping_cart': {},
        'flow': [],
        'is_admin': is_admin,
        'locked': False
    }
    db_handler.save(user_data)
    msg = f'用户{username}注册成功！'
    logger.info(msg)
    return True, msg
#登陆接口
def login_interface(username,password):
    #查看用户是否存在
    user_data = db_handler.select_data(username)
    if not user_data:
        return False,f'\n用户{username}不存在！请重新输入！',False

    if not password == user_data.get('password'):
        return False,'\n用户名或密码错误',False

    if user_data.get('locked'):
        return False,f'用户{username}已被冻结！',False

    msg = f'用户{username}登陆成功！'
    logger.info(msg)
    return True,msg,user_data.get('is_admin')
