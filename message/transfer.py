import socket
from DSPProject import settings
import paramiko
class Functions:
    #往单个远程服务器传送图片
    @classmethod
    def send_pic_to_server(cls, web_server_info, file_path):
        file_dir = file_path.rsplit('.', 1)[0]    #图片所在文件夹

        #链接远程服务器
        # web_server_info = settings.WEB_SERVER_INFO
        ssh=paramiko.Transport((web_server_info["Host"]))
        ssh.connect(username = web_server_info["Username"], password = web_server_info["Password"])
        sftp=paramiko.SFTPClient.from_transport(ssh)

        try:
            sftp.put(file_path, file_path)
            sftp.chown(file_path,1000,1000)
            sftp.close()
        except IOError:
            """
            爲什麼要修改權限，因爲創建的路徑和複製的文件的所有者是root
            因爲上面配置的登陸者是root，但是用戶訪問服務器沒有root的權限
            所以是訪問不了這個路徑的，所以需要將路徑和文件的權限修改，
            至於修改到哪個用戶權限下，看服務器是在哪個賬戶下運行
            """
            sftp.mkdir(file_dir)  #新建路徑
            sftp.chown(file_dir,1000,1000)  #修改路徑的權限
            sftp.put(file_path, file_path)
            sftp.chown(file_path,1000,1000)

    #往多个其他服务器传送图片
    @classmethod
    def send_pic_to_another_servers(cls, web_server_infos, file_path):
        #获取正在访问的服务器地址
        host_name = socket.gethostname()
        server_ip = socket.gethostbyname(host_name)

        #获取到其他服务器的信息字典
        for app in web_server_infos:
            if web_server_infos[app]["Host"] == server_ip:
                del web_server_infos[app]
                break
        another_server_infos = web_server_infos
        # picturename = ''
        #往多个服务器传送图片
        for app in another_server_infos:#将图片存入其他服务器
            # file_path = "/home/work/ksxing_data/test_img/%s"  %picturename
            try:
                Functions.send_pic_to_another_servers(web_server_infos, file_path)
            except:
                pass

            cls.send_pic_to_server(another_server_infos[app], file_path)
