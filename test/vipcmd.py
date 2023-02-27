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
        bat = "./temp.bat"
        with open(bat,'w') as fp: 
            fp.write(cmd)
    except Exception as e:
        traceback.print_exc()
        raise e
    finally:
        if f:
            f.close()
 
    try:
        shell = "temp.vbs"
        with open(shell,'w') as f:
            source='''cwd = CreateObject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path\n
path = cwd & "\\temp.bat"\n
Set shell = CreateObject("Shell.Application")\n
shell.ShellExecute path,"","","runas",1\n
WScript.Quit
                    '''
            f.write(source)

        sp = subprocess.Popen(
            shell,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # print("[PID] %s: %s" % (sp.pid, cmd))
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
        
        runAdmin(sys.argv[1])
    else:
        runAdmin('@echo off && @echo sb && @pause')