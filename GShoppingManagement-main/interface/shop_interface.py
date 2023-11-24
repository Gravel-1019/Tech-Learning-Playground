"""
购物相关接口
"""
from db import db_handler
from interface import bank_interface
from lib import common

logger = common.get_logger('shopping')
#查询商品接口
def check_goods_interface(goods_filename):
    goods = db_handler.select_data(goods_filename,is_user=False)
    if not goods:
        logger.error(f'商品文件{goods_filename}丢失！')
    return goods

#购物车接口
def add_shop_cart_interface(username,shopping_cart):
    user_data = db_handler.select_data(username)
    shopping_cart_file = user_data['shopping_cart']
    for name in shopping_cart.keys():
        if name in shopping_cart_file:
            shopping_cart_file[name]['数量'] += shopping_cart.get(name).get("数量")
        else:
            shopping_cart_file[name] = shopping_cart.get(name)

    db_handler.save(user_data)
    msg = f'用户{username}购物车添加成功！'
    logger.info(msg)
    return True,msg

#结算接口
def close_account_interface(username,shopping_cart):
    total = 0
    for good_info in shopping_cart.values():
        price = good_info.get('price')
        num = good_info.get('数量')
        total += price * num
    flag,msg = bank_interface.pay_interface(username,total)
    return flag,msg,total

#查看购物车接口
def check_shop_cart_interface(username):
    user_data = db_handler.select_data(username)
    shop_cart_file = user_data.get('shopping_cart')
    return shop_cart_file

#清空购物车功能
def clean_shop_cart_interface(username):
    user_data = db_handler.select_data(username)
    user_data['shopping_cart'] = {}
    db_handler.save(user_data)
    msg = f'用户{username}清除购物车成功！'
    logger.info(msg)
    return msg
