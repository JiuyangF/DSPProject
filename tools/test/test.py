import os

import paramiko

#
# def testa():
#     s = [1,2,3,4,5,6,55,5,5,53,3,34]
#     print(s)
#     b = {}
#     s.sort()
#
#     st = set(s)
#     print(st,s)
#     a=[1,2,4,2,4,5,7,10,5,5,7,8,9,0,3]
#
#     a.sort()
#     print(a,a[::-1])
#
#     last=a[-1]
#     for i in range(len(a)-2,-1,-1):
#         print(i)
#         if last == a[i]:
#             del a[i]
#         else:
#             last =a[i]
#     print(a)
#
#     for i in range(len(a)-2,-1,-1):
#
#         if last==a[i]:
#
#             del a[i]
#
#         else:last=a[i]
#
#     sdfsa = {'kl':'das','s':'d','1':'dfsa',1:'ds'}
#     print("sdfsa",sdfsa)
#     print(a)
#     a= 1
#     try:
#         b =a
#     except:
#         s =9
#     a= 3
#     print(a,b)
#
#     import random
#     ee = random.random()
#     e = random.randint(1,89)
#     s  = random.randrange(200,87000,10)
#     sd = random.uniform(22,546)
#     print(e,s,ee,sd)
#
#     alist = [1,2,3,4]
#     b = alist
#     print(b)
#     alist.append(5)
#     print(b,alist)
#
#     a = 3
#     b= a
#     a = 4
#     print(a,b)
#
# def test_os(path):
#     for child in os.listdir(path):
#         cpath = os.path.join(path,child)
#         print(cpath)
#         if os.path.isdir(cpath):
#             test_os(cpath)
#         else:
#             print(cpath)
#
# # test_os('D:\JiuyangLearn\PythonProject\django-blog-tutorial-master\comments\migrations')
#
# def test_ossuper(p_path):
#     # child = os.listdir(p_path)
#     for child in os.listdir(p_path):
#         c_path = os.path.join(p_path,child)
#         if os.path.isdir(c_path):
#             test_ossuper(c_path)
#         else:
#             print(c_path)
# # test_ossuper("D:\JiuyangLearn\PythonProject\django-blog-tutorial-master\comments\migrations")
#
# def test_b():
#     A0 = dict(zip(('a', 'b', 'c', 'd', 'e'), (1, 2, 3, 4, 5)))
#     print(A0)

# test_b()
web_server_info={'Host':'172.31.33.69',
                 'Username':'root',
                 'Password':'syswin#123'}
local_file = 'D:\\work\\rztest.txt'
file_path = '/media/spiders_file/rztest.txt'
def send_pic_to_server(web_server_info, file_path):
    file_dir = file_path.split('/', 1)[0]  # 图片所在文件夹
    print(file_dir,file_path)

    # 链接远程服务器
    # web_server_info = settings.WEB_SERVER_INFO
    ssh = paramiko.Transport((web_server_info["Host"]))
    ssh.connect(username=web_server_info["Username"], password=web_server_info["Password"])
    sftp = paramiko.SFTPClient.from_transport(ssh)

    try:
        sftp.put(localpath=local_file, remotepath=file_path)
        print("first  ")
        sftp.chown(file_path, 1000, 1000)
        sftp.close()
    except IOError:
        """
        爲什麼要修改權限，因爲創建的路徑和複製的文件的所有者是root
        因爲上面配置的登陸者是root，但是用戶訪問服務器沒有root的權限
        所以是訪問不了這個路徑的，所以需要將路徑和文件的權限修改，
        至於修改到哪個用戶權限下，看服務器是在哪個賬戶下運行
        """
        # sftp.mkdir(file_dir)  # 新建路徑
        print('essssss')
        sftp.chown(file_dir, 1000, 1000)  # 修改路徑的權限
        sftp.put(local_file, file_path)
        sftp.chown(file_path, 1000, 1000)

send_pic_to_server(web_server_info, file_path)
