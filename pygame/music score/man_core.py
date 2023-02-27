import pyautogui as pau
import keyboard
import time

up_num=['+'+str(i) for i in range(1,8)]
up_key=list('qwertyu')
down_num=['-'+str(i) for i in range(1,8)]
down_key=list('zxcvbnm')
mid_key=list('asdfghj')

map_num2char={}
for i,j in zip(up_num,up_key):
    map_num2char[i]=j
for i,j in zip(down_num,down_key):
    map_num2char[i]=j


core='guitar.txt'
with open(core,'r') as fp:
    data=fp.read()
    
ctrl_str=list(map(str,range(0,10)))+['/','(',')','/','+','-',]

dp=''
for i in data:
    if i in ctrl_str:
        dp+=i   

for k,v in map_num2char.items():
    dp=dp.replace(k, v)
for k,v in zip('1234567',mid_key):
    dp=dp.replace(k, v)
dp=dp.replace('(',' ')
dp=dp.replace(')',' ')
         
dp_sp=list(filter(bool,dp.split('/')))
for n,_ in enumerate(dp_sp):
    dp_sp[n]=list(filter(bool,_.split(' ')))

bpm=193
shifting=0.1
pau.FAILSAFE = True
note_stop=60/bpm-shifting
#note_stop=0

while 1:
    if keyboard.is_pressed('home'):
        op=pau.confirm(text=f'开始演奏{core}', title='auto play', buttons=['OK', 'Cancel'])
        if op=='OK':
            break

for _ in dp_sp:
    for __ in _: # cnq j
        
        if len(__)>1:
            pau.press(list(__))
        else:
            pau.press(__)
        while 1:
            if keyboard.is_pressed('space') or keyboard.is_pressed('enter'):
                break
            
            
            
        # time.sleep(note_stop/len(_))
        
        # if len(__)>1:
        #     for ___ in __:
        #         pau.keyDown(___)
        #     time.sleep(note_stop/len(_))
        #     for ___ in __:   
        #         pau.keyUp(___)
        
        
        
        
        
        
'''


'''

























