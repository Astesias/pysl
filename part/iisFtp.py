from ftplib import FTP

####### 连接 FTP 服务器
# 如果 FTP 不用用户名密码就直接可以访问，那就是用的默认用户名 Anonymous，密码为空。
def conn_ftp():
    '''
     作用：连接ftp服务器
     参数：无
     返回：ftp服务器连接的对象
    '''
    
    # FTP连接信息
    ftp_ip = '10.20.85.35'
    # 默认端口21
    ftp_port = 21
    # 如果未指定，使用默认用户名为Anonymous，密码为空
    ftp_user = "Anonymous"
    # ftp_user = "zcz"
    ftp_password = ""

    ftp = FTP()
    # 连接ftp
    ftp.connect(ftp_ip, ftp_port)
    # ftp登录
    ftp.login(ftp_user, ftp_password)
    # 查看欢迎信息
    print(ftp.getwelcome())
    
    return ftp
    


###### 进入指定目录并显示文件信息
def display_dir(ftp, path):
    '''
     作用：进入并展示指定的目录内容
     参数1：ftp连接对象
     参数2：要展示的目录
     返回：无
    '''
    
    # 进入指定目录
    ftp.cwd(path)
    # 显示当前所在位置
    print("当前所在位置为：")
    print(ftp.pwd())
    # 展示目录内容
    print("\n显示目录内容：")
    print(ftp.dir())
    # 展示目录下的文件名，*文件夹和文件都会显示
    print("\n文件和文件夹名为：")
    for i in ftp.nlst():
        print(i)




######  区分文件和文件夹名
def diff_dir(ftp, path):
    '''
     作用：区分文件和文件夹
     参数1：ftp连接对象
     参数2：要展示的目录
     返回：无
    '''
    
    # 进入指定目录
    ftp.cwd(path)
    # 显示当前所在位置
    print("当前所在位置为：")
    print(ftp.pwd())
    # 展示目录内容
    print("\n显示目录内容：")
    dirs = []
    ftp.dir(".", dirs.append)
    for i in dirs:
        # 区分文件和文件夹 文件夹中含有drw开头
        print(i)
        if("drw" in i):   
            print("目录为：" + i.split(" ")[-1])
        else:
            print("文件为：" + i.split(" ")[-1])



#### 文件夹名包含空格处理
def get_dir_name(s):
    '''
     作用：需要文件或文件夹名
     参数1：需要截取的字符串
     返回：文件或文件夹名
    '''
    dir_name = ""
    k = 0
    record = ""
    for i in s:
        if(record == " " and i != " "):
            k = k + 1;
        if(k >= 3):
            dir_name = dir_name + i;
        record = i
        
    print(dir_name)
    return dir_name





# iis

ftp = conn_ftp()

path = "/"
diff_dir(ftp, path)

# path = "/"   #指定ftp目录
# display_dir(ftp, path)


# # 测试两条数据
# get_dir_name("05-25-22  02:52PM       <DIR>          test")
# get_dir_name("05-25-22  03:32PM                89098 hello.txt")

# ####   ftp上传文件
# ftp = FTP(host='127.0.0.1', user='zcz', passwd='zcz') #创建
# ftp.cwd('/test') #上传路径
# fd = open('D:\\ksafe\\ksoft\\scripts\\py\\test.xlsx', 'rb') #以只读的方式打开要上传的文件
# ftp.storbinary('STOR test.xlsx', fd) #上传文件
# fd.close()
# ftp.quit() #退出登录
# ftp.close() #关闭连接


# ####   ftp下载文件
# ftp = FTP(host='127.0.0.1', user='zcz', passwd='zcz') #创建
# fd = open('D:/test/test.xlsx', 'wb') #以只写的方式打开要下载的文件及目录
# ftp.cwd('/test/') #服务器下载路径
# ftp.retrbinary('RETR test.xlsx', fd.write, 2048) #下载文件
# #ftp.retrbinary('RETR /test/test.xlsx', fd.write, 2048) #下载文件
# fd.close()
# ftp.quit() #退出登录
# ftp.close() #关闭连接

