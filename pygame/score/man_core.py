import pyautogui as pau
import keyboard
import time
import re
from pysl import backref_dict,flatten,path2filename,admin_monitor,is_admin
    
map_dict=backref_dict(
            {'+1': 'q',
             '+2': 'w',
             '+3': 'e',
             '+4': 'r',
             '+5': 't',
             '+6': 'y',
             '+7': 'u',
                    '1': 'a',
                    '2': 's',
                    '3': 'd',
                    '4': 'f',
                    '5': 'g',
                    '6': 'h',
                    '7': 'j',
                         '-1': 'z',
                         '-2': 'x',
                         '-3': 'c',
                         '-4': 'v',
                         '-5': 'b',
                         '-6': 'n',
                         '-7': 'm'
            },k2v=True)

class AutoScore:
    
    PHONE_TYPE=0
    WIN_TYPE=1
    CLASS_TYPE=-1
    
    AUTO_MODE=0
    HALF_AUTO_MODE=1
    NO_AUTO_MODE=-1
    
    def __init__(self,score_path,type=PHONE_TYPE):
        self.score_path=score_path
        self.name=path2filename(score_path)
        self.type=type
        self.form_data=self._load(type)
        self._iter,self._data=self._iter_score(self.form_data)
     
    def iter(self):
        return self._iter
    def save(self,dst,type=CLASS_TYPE):
        with open(dst,'w') as fp:
            for _ in self.iter():
                fp
                pass
        pass
    def play(self,mode=AUTO_MODE,bpm=None,shifting=0):
        if bpm:
            step=60/bpm
        else:
            step=60/200
        while 1:
            if keyboard.is_pressed('home'):
                # op=pau.confirm(text=f'开始演奏 {self.name}', title='auto play', buttons=['OK', 'Cancel'])
                # if op=='OK':
                    break
        if mode!=self.NO_AUTO_MODE:
            for _ in self.iter():
                for __ in _: # [cnq j]
                    sclen=len(__)
                    for ___ in __: # cnq j
                        if len(___)>1:
                            pau.press(list(___))
                        else:
                            pau.press(___)     
                        if mode==self.HALF_AUTO_MODE:
                            while 1:
                                if keyboard.is_pressed('space') or keyboard.is_pressed('enter'):
                                    break
                        else:
                            if sclen==1:
                                time.sleep(step/2)
                            else:
                                time.sleep(step/4/sclen)

    def _load(self,type):
        return self.__type_load(self.type)
        
    def _switch_type(self,type_id):
        pass
    
    def _iter_score(self,dp):
        dp_s=dp.split('|')
        dp_g=[]
        
        i=0
        while 1:
            e=dp_s[i:i+4]
            if e:
                dp_g.append(e)
            else:
                break
            i+=4
        
        dp_sp=[]
        for _ in dp_g:
            temp=[]
            for __ in _:
                temp.append(list(filter(bool,__.split(' '))))
            dp_sp.append(temp)
        return iter(dp_sp),dp_sp
    
    
    def __type_load(self,type):
        dp=self.__preload(self.type)
        if self.type==self.PHONE_TYPE:
            for k,v in map_dict.items():
                dp=dp.replace(k,v)
        dp=dp.replace('(','')
        dp=dp.replace(')|','|')
        dp=dp.replace(')',' ')
        return dp

    def __preload(self,type):
        with open(self.score_path) as fp:
            data=fp.read()  
        
        ctrl_str=self.__preload_ctrlchar(self.score_path,type)
        dp=self.__preload_filter(data,ctrl_str)
        dp=self.__preload_getrest(dp)
        return dp
            
    def __preload_ctrlchar(self,path,type):
        if type==self.PHONE_TYPE:
            return list(map(str,range(0,10))) + ['(',')','/','+','-',' ']
        elif type==self.WIN_TYPE:
            return list('qwertyuasdfghjzxcvbnm') + ['(',')','/',' ']
        elif type==self.CLASS_TYPE:
            return list('qwertyuasdfghjzxcvbnm') + ['(',')','|','#']
        
    def __preload_filter(self,data,ctrl_str):
        dp=''
        for i in data:
            try:
                if i.lower() in ctrl_str:
                    dp+=i.lower()
            except:
                if i in ctrl_str:
                    dp+=i
        return dp
    
    def __preload_getrest(self,dp):
        dp=re.sub('(?<=/) +(?=/)','#',dp)
        dp=dp.replace(' ','')
        dp=dp.replace('/','|')
        if dp[0]=='|':
            dp='$'+dp
        if dp[0-1]=='|':
            dp=dp[:-1]
        return dp
    

if __name__ == '__main__':
    if is_admin():
        a=AutoScore('吉他与孤独与蓝色星球.txt',type=AutoScore.PHONE_TYPE)
        b=AutoScore('拼凑的断音.txt',type=AutoScore.WIN_TYPE)
        
        b.play(mode=AutoScore.AUTO_MODE,bpm=150)
    else:
        admin_monitor(__file__)




'''
class
mode switch
load 
iter
write

'''



