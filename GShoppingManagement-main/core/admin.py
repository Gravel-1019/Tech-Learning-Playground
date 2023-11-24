'''
管理员视图层
'''
from core import src
from interface import admin_interface
#添加账户功能
def add_user():
    is_admin = input("是否添加管理员(y or n)：").strip().lower()
    if is_admin == 'y':
        src.register(True)
    else:
        src.register()


#冻结账户功能
def lock_user():
    while True:
        lock_username = input(f"尊贵的管理员{src.logged_user}，请输入您想冻结/解冻的用户名：").strip()
        is_lock = input("按任意键确认/n退出：").strip().lower()
        if is_lock == 'n':
            break

        if src.logged_user == lock_username:
            print(f'\n尊贵的管理员{src.logged_user}，您不能冻结自己！！！\n')
            continue

        flag,msg = admin_interface.lock_user_interface(lock_username)
        print(msg)
        if flag:
            break


#给用户充值
def recharge_to_user():
    username = input(f'\n尊贵的管理员{src.logged_user}，请输入需要充值的用户名：').strip()
    src.recharge(username)

func_dic = {
    '0' : ('返回首页',),
    '1' : ('添加账户功能',add_user),
    '2' : ('冻结/解冻账户功能',lock_user),
    '3' : ('给用户充值功能',recharge_to_user)
}


#管理员主功能
def main():
    while True:
        print("管理员功能".center(20,'='))
        for num in func_dic:
            print(f'{num} {func_dic.get(num)[0]}'.center(20,' '))
        print("我是有底线的".center(20,'='))
        opt = input("请输入功能编号：").strip()
        if opt not in func_dic:
            print("此功能不存在！")
            continue
        if opt == '0':
            break
        func_dic.get(opt)[1]()