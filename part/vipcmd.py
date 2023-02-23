# !/usr/bin/python3
# coding: utf-8
import os
import sys
import subprocess
import traceback
 
 
def runAdmin(cmd, timeout=1800000):
    # 这一段是将要执行的cmd命令写入.bat, 如果已经有创建好的.bat， 则这一段可以注释掉
    f = None
    try:
        bat = "D:/Desktop/.py/temp/RestartInternet.bat"
        f = open(bat, 'w')
        f.write(cmd)
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        if f:
            f.close()
 
    try:
        shell = "D:/Desktop/.py/temp/shell.vbs"
        sp = subprocess.Popen(
            shell,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("[PID] %s: %s" % (sp.pid, cmd))
        sp.wait(timeout=timeout)
 
        stderr = str(sp.stderr.read().decode("gbk")).strip()
        stdout = str(sp.stdout.read().decode("gbk")).strip()
        print(stdout)
        if "" != stderr:
            raise Exception(stderr)
        if stdout.find("失败") > -1:
            raise Exception(stdout)
    except Exception as e:
        raise e
        
if __name__ == '__main__':
    
    if len(sys.argv)==2:
        
        runAdmin(f'cd /d D:/Desktop/.py/temp/  &\
                 {sys.argv[1]}                  \
                ')
    else:
        runAdmin('cd /d D:/Desktop/.py/temp/   &\
                  echo sb                      &\
                  pause                         \
               ')