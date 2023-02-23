import tkinter as tk
import time
import pygame
import numpy as np
import os
import random
import threading
import tkinter.filedialog
# from pysl import path2filename

#global playing mu_name 
        
def path2filename(path):
    if type(path)!=type('str'):
        raise TypeError('path is a str,not {}'.format(type(path)))
    return path[path.rfind('\\')+1:]


class music_palyer():
    
    num=0
    
    def __init__(self,path=''):
        
        pygame.mixer.init()
        
        music_palyer.num+=1
        
        self.path = path
        self.playing=False
        self.pathflag=1
        self.pauseflag=1
        self.stopflag=0
        self.stopflaglastmusic=0
        
        try:
            with open('./playercfg.txt','r') as fp:
                user_path=fp.read()
                self.path=user_path
        except:
            pass
        
        # self.mu_name='None'
        
        self.root=tk.Tk()
        self.root.title('Music Player ({})'.format(music_palyer.num))
        self.root.geometry('560x140+400+300')
        self.root.resizable(0,0)
        
        self.root.protocol('WM_DELETE_WINDOW',self.close_window)
        self.pause_resume=tk.StringVar(self.root,value='NotSet')
        
        self.button_play=tk.Button(self.root,text='Play',command=self.button_play_click)
        self.button_play.place(x=40,y=20,width=100,height=40)
        
        self.button_stop=tk.Button(self.root,text='Stop',command=self.button_stop_click)
        self.button_stop.place(x=160,y=20,width=100,height=40)
        self.button_stop['state']='disabled'
        

        self.button_pause=tk.Button(self.root,text='Pause',textvariable=self.pause_resume,command=self.button_pause_click)
        self.button_pause.place(x=280,y=20,width=100,height=40)    
        self.button_pause['state']='disabled'
        
        self.button_next = tk.Button(self.root, text='Next', command=self.button_next_click)
        self.button_next.place(x=400, y=20, width=100, height=40)
        self.button_next['state'] = 'disabled'
        
        self.mu_name = tk.StringVar(self.root, value='暂时没有播放音乐...')
        self.labelName = tk.Label(self.root, textvariable=self.mu_name)
        self.labelName.place(x=0, y=80, width=540, height=40)
        
        self.root.mainloop()
        
    def play(self): #process1
        music_pathes=[ self.path+'\\' +mu for mu in os.listdir(self.path) if mu.endswith(('mp3','wav')) ]
        mu_len=len(music_pathes)
        pygame.mixer.init()

        while self.playing:
            if self.pauseflag:
                if not pygame.mixer.music.get_busy():
                    
                    
                    # print(type(next_mu))
                    if self.stopflag:
                        pygame.mixer.music.load(self.stopflaglastmusic.encode())
                        self.stopflag=0
                        pygame.mixer.music.play(1)
                        self.mu_name.set(path2filename(self.stopflaglastmusic).rstrip('.mp3'))
                        
                    else:
                        self.next_mu=random.choice(music_pathes)
                        pygame.mixer.music.load(self.next_mu.encode())
                        try:
                            pygame.mixer.music.play(1)
                            self.mu_name.set(path2filename(self.next_mu).rstrip('.mp3'))
                        except pygame.error:
                            print(self.next_mu+': 不支持的格式')
                    
            else:
                time.sleep(0.3)
                
    def close_window(self):
        self.playing=False
        try:
            pygame.music.stop()
            pygame.mixer.quit()
            
        except:
            pass
        
        self.root.destroy()
        
    def button_play_click(self):

        if self.pathflag:
            if not self.path:
                self.path=tk.filedialog.askdirectory()
                if tk.messagebox.askquestion(title='设置', message='设为默认文件夹？')=='yes':
                    self.pathflag=0
                    with open('./playercfg.txt','w') as fp:
                        fp.write(self.path)
            if not self.path:
                return
        self.playing=True
        t=threading.Thread(target=self.play)
        t.start()
        
        self.button_play['state']='disabled'
        self.button_stop['state']='normal'
        self.button_pause['state']='normal'
        self.button_next['state']='normal'
        self.pause_resume.set('Pause')
            
    def button_stop_click(self):
        self.playing=False
        self.stopflaglastmusic=self.next_mu
        self.stopflag=1
        pygame.mixer.music.stop()
        self.mu_name.set('stoping')
        
        self.button_play['state']='normal'
        self.button_pause['state']='disabled'
        self.button_next['state']='disabled'        
        
    def button_pause_click(self):
     
        if self.pause_resume.get() == 'Pause':
            
            self.pauseflag=0
            pygame.mixer.music.pause()
            self.pause_resume.set('Resume')
            
            
        elif self.pause_resume.get() == 'Resume':
    
            pygame.mixer.music.unpause()
            self.pause_resume.set('Pause')

    def button_next_click(self):

        self.pauseflag=1
        self.playing = False
        pygame.mixer.music.stop()
        
        pygame.mixer.quit()
        self.button_play_click()


a=music_palyer()
pygame.mixer.quit()
        
        
        
        
    
                

                