# -*- coding: utf-8 -*-

import telnetlib

import time

'''Telnet远程登录：Windows客户端连接Linux服务器'''

# 配置选项
Host = '172.31.33.69'  # Telnet服务器IP
username = 'jiuyang'  # 登录用户名
password = 'syswin#123'  # 登录密码
finish = b'$ '  # 命令提示符（标识着上一条命令已执行完毕）

# 连接Telnet服务器
tn = telnetlib.Telnet(Host)
# tn.write('\n'.encode())
print("telnet begin")
# 输入登录用户名
tn.read_until('bogon login:'.encode())
tn.write((username + '\n').encode())
print("input password")
# 输入登录密码
tn.read_until('Password:'.encode())
tn.write((password + '\n').encode())
print("telnet success")
# 登录完毕后，执行ls命令

tn.read_until(finish)
time.sleep(0.5)
# tn.read_until(finish)
result = tn.read_very_eager()

print(result.decode())
# ls命令执行完毕后，终止Telnet连接（或输入exit退出）
tn.write(b'\n')
tn.read_until(finish)
tn.close()  # tn.write('exit\n')