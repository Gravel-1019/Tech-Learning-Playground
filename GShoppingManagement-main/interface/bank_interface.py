"""
银行相关接口
"""
from db import db_handler
from conf import settings
from datetime import datetime
from core import src
from lib import common


logger = common.get_logger('bank_logger')
import json
#充值接口
def recharge_interface(username,amount):
    user_data = db_handler.select_data(username)
    if not user_data:
        return True,f'\n尊贵的管理员{src.logged_user}，您输入的用户{username}不存在！'

    user_data['balance'] += amount

    #记录流水
    msg = f'\n{datetime.now().replace(microsecond=0)}用户{username}充值{amount}元！\n当前余额为{user_data["balance"]}元！'
    user_data['flow'].append(msg)

    db_handler.save(user_data)
    logger.info(msg)
    return True,msg

#提现接口
def withdraw_interface(username,amount):
    user_data = db_handler.select_data(username)
    balance = user_data.get('balance')
    service_fee = settings.RATE * amount
    if balance < (service_fee + amount):
        return False,'\n余额不足，提现失败！'

    user_data['balance'] -= (amount - service_fee)

    # 记录流水
    msg = f'\n{datetime.now().replace(microsecond=0)}用户{username}提现{amount}元！' \
          f'\n手续费为{service_fee}元！' \
          f'\n当前余额为{user_data.get("balance")}元！\n'
    user_data["flow"].append(msg)


    db_handler.save(user_data)
    logger.info(msg)
    return True,msg

#查看余额接口
def check_balance_interface(username):
    user_data = db_handler.select_data(username)
    return f'\n{username}账户中还有{user_data["balance"]}元'

#转账接口
def transfer_interface(username,to_username,amount):
    user_data = db_handler.select_data(username)
    to_user_data = db_handler.select_data(to_username)

    #判断to_username是否存在
    if not to_user_data:
        return False,f'\n目标用户：{to_username} 不存在！'
    if user_data.get("balance") < amount:
        return False,f"\n无法转账，用户{username}余额不足！"

    user_data['balance'] -= amount
    to_user_data['balance'] += amount

    #记录流水
    msg = f'\n{datetime.now().replace(microsecond=0)}' \
          f'\n用户：{username}给用户：{to_username}成功转账{amount}元'\
          f'\n当前余额为{user_data.get("balance")}元！\n'
    user_data['flow'].append(msg)
    to_msg = f'\n{datetime.now().replace(microsecond=0)}' \
          f'\n用户：{to_username}收到用户：{username}成功转账{amount}元' \
          f'\n当前余额为{to_user_data.get("balance")}元！\n'
    to_user_data['flow'].append(to_msg)
    db_handler.save(user_data)
    db_handler.save(to_user_data)
    logger.info(msg)
    return True, msg

#查看流水接口
def check_flow(username):
    user_data = db_handler.select_data(username)
    flow_list = user_data.get('flow')
    return True,flow_list

#支付接口
def pay_interface(username,total):
    user_data = db_handler.select_data(username)
    if user_data.get('balance') < total:
        msg = f'\n用户{username}余额不足，无法支付{total}元,支付失败！！！'
        logger.warning(msg)
        return False,msg

    user_data['balance'] -= total
    msg = f"\n{datetime.now().replace(microsecond=0)}用户{username}消费{total}元，" \
          f"当前余额为{user_data.get('balance')}元"
    user_data['flow'].append(msg)
    db_handler.save(user_data)
    logger.info(msg)
    return True,msg


