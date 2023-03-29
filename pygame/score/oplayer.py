import re
import os
import time
import keyboard
from cfgset import setcfg
from keypresser import press_keys
from utils import backref_dict,path2filename,admin_monitor,is_admin


map_dict=backref_dict(
            {'+1': 'q',
             '+2': 'w',
             '+3': 'e',
             '+4': 'r',
             '+5': 't',
             '+6': 'y',
             '+7': 'u',
                         '-1': 'z',
                         '-2': 'x',
                         '-3': 'c',
                         '-4': 'v',
                         '-5': 'b',
                         '-6': 'n',
                         '-7': 'm',
                    '1': 'a',
                    '2': 's',
                    '3': 'd',
                    '4': 'f',
                    '5': 'g',
                    '6': 'h',
                    '7': 'j',
            },k2v=True)

class AutoScore:
    
    PHONE_TYPE=0
    WIN_TYPE=1
    CLASS_TYPE=-1
    
    AUTO_MODE=0
    HALF_AUTO_MODE=1
    NO_AUTO_MODE=-1
    
    def __init__(self,score_path,type=WIN_TYPE,score_dir='scoretxt/'):
        self.score_path=os.path.join(score_dir,score_path)
        self.name=path2filename(score_path)
        self.type=type
        self.form_data=self._load(type)
        self._iter,self._data=self._iter_score(self.form_data)
        self._play=False
     
    def iter(self):
        return self._iter
    def save(self,dst,type=CLASS_TYPE):
        with open(dst,'w',encoding='utf8') as fp:
            for _ in self.iter():
                fp
                pass
        pass
    def play(self,mode=AUTO_MODE,bpm=None,shifting=0):
        if bpm:
            step=60/bpm*192/210
        else:
            step=60/210

        while 1:
            if keyboard.is_pressed('home'):
                self._play=True
                break
        while 1:
            if mode!=self.NO_AUTO_MODE and self._play:
                for _ in self.iter():
                    for __ in _: 
                        sclen=len(__)
                        for ___ in __:
                            press_keys(___)
                            if mode==self.HALF_AUTO_MODE:
                                while 1:
                                    if keyboard.is_pressed('space') or keyboard.is_pressed('enter'):
                                        break
                            else:
                                if sclen==1:
                                    time.sleep(step)
                                else:
                                    time.sleep(step/sclen)
                self._play=False
            else:
                break

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
        with open(self.score_path,encoding='utf8') as fp:
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
            if dp[1]=='#':
                dp=dp[1:]
            else:
                dp='#'+dp
        if dp[-1]=='|':
            dp=dp[:-1]
        return dp
    

if __name__ == '__main__':
    # print(*zip(list(range(len(os.listdir('./scoretxt')))),os.listdir('./scoretxt')),sep='\n')
    
    try:
        if is_admin():
            print('################################\nCreate by ysl ,Copyright 2023 ©\n')
            while 1:
                cfg=setcfg()
                if not cfg:
                    print('添加乐谱后再打开')
                    time.sleep(5)
                    break
                print('_______________________________')
                for i,j in enumerate(os.listdir('./scoretxt')):
                    print(f'{i+1}. {j}')
                print('_______________________________')
                    
                index=int(input('演奏曲目:'))
                sc=os.listdir('./scoretxt')[index-1]
                
                print('\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print(f'准备演奏 {sc}')
                type=cfg[sc]['type']
                print('乐谱类型为 '+('键盘(1)' if type==1 else '手机(0)'))
                bpm=cfg[sc]['bpm']
                if not bpm:
                    print('bmp未设置，默认为192')
                else:
                    print(f'bpm{bpm}')
                dd=AutoScore(sc,type=type)
                print('按home键开始演奏')
                print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
                
                dd.play(mode=AutoScore.AUTO_MODE,bpm=bpm)
    
        else:
            admin_monitor(__file__)
    except:
        import traceback
        with open('log.txt','w',encoding='utf8') as fp:
            fp.write(traceback.format_exc())

'''
class
mode switch
load 
iter
write

'''

'''
210 gt
210 1
210 toa

            # aa=AutoScore('吉他与孤独与蓝色星球.txt',type=AutoScore.PHONE_TYPE)
            # bb=AutoScore('拼凑的断音.txt',type=AutoScore.WIN_TYPE)
            # cc=AutoScore('1.txt',type=AutoScore.WIN_TYPE)

'''


