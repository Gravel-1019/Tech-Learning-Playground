"""
用户视图层
"""
from lib import common
from  interface import user_interface,bank_interface,shop_interface
logged_user = None
logged_admin = False

#0、退出
def sign_out():
    print("\n感谢使用，欢迎下次光临")
    exit()


#1、注册功能
def register(is_admin=False):
    while True:
        print("\n注册")
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()
        is_register = input("按任意键确认/n退出：").strip().lower()
        if is_register == 'n':
            break
        if password != re_password:
            print("\n两次输入的密码不一致")
            continue
        #判断用户名是否合法
        import re
        if not re.findall('^[a-zA-z]\w{2,9}$',username):
            print("\n用户名长度必须为3-10个字符\n只能由字母、数字、下划线组成，并只能以字母开头")
            continue
        #校验密码强度
        if not re.findall('^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,16}$',password):
            print("\n密码太弱，必须包含大写字母、小写字母和数字，并且长度必须为8-16位！")
            continue

        # 加密
        password = common.pwd_to_sha256(password)

        flag,msg = user_interface.register_interface(username,password,is_admin)
        print(msg)
        if flag:
            break




#2、登录功能
def login():
    print("\n登陆")
    while True:
        # 输入用户名和密码
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        is_login = input('按任意键确认/n退出：').strip().lower()


        if is_login == 'n':
            break

        # 加密
        password = common.pwd_to_sha256(password)
        # 查询用户是否存在
        flag, msg,is_admin = user_interface.login_interface(username, password)

        print(msg)
        if flag:
            global logged_user,logged_admin
            logged_user = username
            logged_admin = is_admin
            break



#3、充值功能
@common.login_auth
def recharge(username=False):
    print("\n充值")
    while True:
        #接收用户输入的充值金额
        amount = input("输入您要充值的金额：").strip()
        is_recharge = input("按任意键确认/n退出：").strip().lower()
        if is_recharge == 'n':
            break

        if not amount.isdigit():
            print("\n请输入正确的金额！")
            continue

        amount =int(amount)
        if amount == 0:
            print("\n充值的金额不能是0！")
            continue
        if not username:
            username = logged_user
        flag,msg = bank_interface.recharge_interface(username,amount)
        print(msg)
        if flag:
            break

@common.login_auth
#4、转账功能
def transfer():
    while True:
        print("\n转账")
        #接受用户名和转账金额
        to_username = input("输入转账目标用户名：").strip()
        amount = input("输入转账金额：").strip()
        is_transfer = input("按任意键确认/n退出：").strip().lower()
        if is_transfer == 'n':
            break

        if not amount.isdigit():
            print("\n请输入正确的金额！")
            continue

        amount =int(amount)
        if amount == 0:
            print("\n转账的金额不能是0！")
            continue
        if logged_user == to_username:
            print("\n不能给自己转账！")
            continue

        flag,msg = bank_interface.transfer_interface(
            logged_user,to_username,amount
        )
        print(msg)
        if flag:
            break


@common.login_auth
#5、提现功能
def withdraw():
    print("\n提现")
    while True:
        # 接收用户输入的提现金额
        amount = input("输入您要提现的金额：").strip()
        is_withdraw = input("按任意键确认/n退出：").strip().lower()
        if is_withdraw == 'n':
            break

        if not amount.isdigit():
            print("\n请输入正确的金额！")
            continue

        amount = int(amount)
        if amount < 500:
            print("\n提现金额不能小于500！")
            continue
        flag, msg = bank_interface.withdraw_interface(logged_user, amount)
        print(msg)
        if flag:
            break

@common.login_auth
#6、查看余额
def check_balance():
    print("\n余额")
    balance = bank_interface.check_balance_interface(logged_user)
    print(balance)

@common.login_auth
#7、查看流水
def check_flow():
    print("\n流水")
    flag,flow_list = bank_interface.check_flow(logged_user)
    if not flow_list:
        print("\n当前用户没有流水！")
    for flow in flow_list:
        print(flow)

# 8、购物功能
@common.login_auth
def shopping():

    # 初始化购物车
    shopping_cart = {}
    # {"韭菜":{"number": "F00001", "name": "韭菜", "price": 2.0, "商品数量": 2},}

    # 1、调用接口层，获取商品数据
    goods = shop_interface.check_goods_interface('goods')

    if not goods:
        print('\n没有商品数据！')
        return


    while True:
        print('欢迎来到沙砾商城'.center(50, '='))
        print(f'{"序号":<10}{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}')
        for indx, good in enumerate(goods):
            print(f'{indx+1:<10}{good.get("number"):<10}{good.get("name"):<10}{good.get("price"):<10}')
        print('24小时为您服务'.center(50, '='))

        opt = input('请选择商品序号(y结算/n退出)：').strip()

        # 如果opt等于n，调用添加购物车接口，把购物车数据写入文件
        if opt == 'n':
            if not shopping_cart:
                break
            flag, msg = shop_interface.add_shop_cart_interface(logged_user, shopping_cart)
            print(msg)
            if flag:
                break

        # 如果用户输入y，调用结算接口
        if opt == 'y':
            if not shopping_cart:
                print('\n没有选择任何商品，无法结算！')
                continue

            flag, msg, total = shop_interface.close_account_interface(logged_user, shopping_cart)
            print(msg)
            if flag:
                print('欢迎光临沙砾商城'.center(72, ' '))
                print('='*72)
                print(f'{"序号":<10}{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}{"商品数量":<10}{"商品总价":<10}')
                for indx, good in enumerate(shopping_cart.values()):
                    print(
                        f'{indx + 1:<10}{good.get("number"):<10}{good.get("name"):<10}{good.get("price"):<10}{good.get("数量"):<10}{good.get("数量") * good.get("price"):<10}')
                print(f'总消费金额：{total}')
                print('='*72)
                print('谢谢惠顾，欢迎下次光临'.center(72, ' '))
                print('请保管好您的小票'.center(72, ' '))
            break

        # 3、判断用户输入的是否是数字
        if not opt.isdigit():
            print('\n请输入正确的商品编号！')
            continue

        # 4、判断用户输入的序号是否存在
        opt = int(opt) - 1
        if opt not in list(range(len(goods))):
            print('\n该商品不存在！')
            continue

        # 5、获取用户选择的商品信息
        good_info = goods[opt]
        name = good_info.get('name')

        # 6、把商品信息添加到用户的购物车
        # 6.1、判断购物车是否存在相同的商品
        if name not in shopping_cart:
            good_info['数量'] = 1
            shopping_cart[name] = good_info
        else:
            shopping_cart[name]['数量'] += 1

        print('\n当前购物车数据：')
        print(f'{"序号":<10}{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}{"商品数量":<10}{"商品总价":<10}')
        for indx, good in enumerate(shopping_cart.values()):
            print(f'{indx + 1:<10}{good.get("number"):<10}{good.get("name"):<10}{good.get("price"):<10}{good.get("数量"):<10}{good.get("数量")*good.get("price"):<10}')

@common.login_auth
#9、查看购物车
def check_shopping_cart():
    print("\n购物车")
    shop_cart_file = shop_interface.check_shop_cart_interface(logged_user)
    if not shop_cart_file:
        print('\n购物车是空的！')
        return
    print('\n当前购物车数据：')
    print(f'{"序号":<10}{"商品编号":<10}{"商品名称":<10}{"商品价格":<10}{"商品数量":<10}{"商品总价":<10}')
    for indx, good in enumerate(shop_cart_file.values()):
        print(
            f'{indx + 1:<10}{good.get("number"):<10}{good.get("name"):<10}{good.get("price"):<10}{good.get("数量"):<10}{good.get("数量") * good.get("price"):<10}')

    opt = input("y付款n退出：").strip().lower()
    if opt == 'y':
        flag,msg,total = shop_interface.close_account_interface(logged_user,shop_cart_file)
        print(msg)
        if flag:
            shop_interface.clean_shop_cart_interface(logged_user)


@common.login_auth
#10、退出账号
def login_out():
    global logged_user,logged_admin
    print(f'{logged_user}已退出登录！')
    logged_user = None
    logged_admin = False


#11、管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.main()
#函数字典
func_dic = {
    '0' : ('退出功能',sign_out),
    '1' : ("注册功能",register),
    '2' : ("登陆功能",login),
    '3' : ("充值功能",recharge),
    '4' : ("转账功能",transfer),
    '5' : ("提现功能",withdraw),
    '6' : ("查看余额功能",check_balance),
    '7' : ("查看流水",check_flow),
    '8' : ("购物功能",shopping),
    '9' : ("查看购物车",check_shopping_cart),
    '10' : ("退出账号",login_out),
    '11' : ("管理员功能",admin),
}

def main():
    while True:
        print("购物管理系统".center(20,'='))

        for num in func_dic:
            if logged_admin:
                print(f'{num} {func_dic.get(num)[0]}'.center(20,' '))
            else:
                if num != '11':
                    print(f'{num} {func_dic.get(num)[0]}'.center(20, ' '))
        print("我是有底线的".center(20,'='))
        opt = input("请输入功能编号：").strip()
        if opt not in func_dic or (not logged_admin and opt == '11'):
            print("此功能不存在！")
            continue


        func_dic.get(opt)[1]()

