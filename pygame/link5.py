import pygame
import cv2
from pysl import cv2_imread

class link_game:
    def __init__(self,player_names=['A','B'],win_link=5):
        self.A_name=player_names[0]
        self.B_name=player_names[1]
        self.linerow=19
        self.loadMap(1.3)
        
    def start(self):
        now_turn=False
        self.displayMap()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        while self.checkWin()==False:
            x=int(input())
            y=int(input())
            self.setKey(now_turn,x,y)
            now_turn=not now_turn
         
            self.displayMap()
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
    def loadMap(self,resize=1):
        
        self.maps=cv2_imread('board.jpg')
        self.maps=cv2.resize(self.maps,(int(1000*resize),int(650*resize)))

        self.sx=69.2*resize
        self.sy=255.3*resize
        ex=578.4*resize
        ey=744.6*resize
        self.block=(ex+ey-self.sx-self.sy)/((self.linerow-1)*2)
        
    def displayMap(self):
        # self.maps[int(self.sx):int(self.sx)+10,int(self.sy):int(self.sy+10)]=255
        cv2.imshow('1',self.maps)
        
    def setKey(self,pnum,x,y):
        x,y=self.getPosition(x,y)

        if pnum: # w
            self.maps[x:x+5,y:y+5]=255
        else:
            self.maps[x:x+5,y:y+5]=0
    
    def getPosition(self,x,y):
        return int(self.sx+x*self.block),int(self.sy+y*self.block)
    
    def checkWin(self):
        return False
    

g1=link_game()
g1.displayMap()
# g1.start()
