import os
import socket
import winreg
from pysl import admin_monitor,is_admin

def main():
    # 管理员模式运行
    #检测主机名，并将主机名作文检测结果的文件名
    hostname = socket.gethostname()
    file = open(r'%s.txt' % hostname, 'w')#保存在当前目录，使用新建模式
      
    #定义检测位置
    sub_key = [
        r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', 
        r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
    ]
      
    software_name = []
    for i in sub_key:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, 
            i, 
            0, 
            winreg.KEY_ALL_ACCESS
        )
        for j in range(0, winreg.QueryInfoKey(key)[0]-1):
            try:
                key_name = winreg.EnumKey(key, j)
                key_path = i + '\\' + key_name
                each_key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, 
                    key_path, 
                    0, 
                    winreg.KEY_ALL_ACCESS
                )
                DisplayName, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                DisplayName = DisplayName.encode('utf-8')
                software_name.append(DisplayName)
            except WindowsError:
                pass
      
     
    software_name = list(set(software_name))
    software_name = sorted(software_name)
      
    for result in software_name:
    	app_name=str(result,encoding='utf-8')
    	file.write(app_name + '\n')
    	print(app_name)
    file.close()
    
if __name__ == '__main__':
    if is_admin():
        main()
    else:
        admin_monitor(__file__)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    