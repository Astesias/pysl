import pyautogui as pg   
import random
import time 
pg.PAUSE = 0.5
pg.FAILSAFE = True
# try:
#     while True:
#         x,y=pg.position()               
#         print(str(x)+" "+str(y)) #输出鼠标的x,y
#         time.sleep(0.1)
# except KeyboardInterrupt:
#     print("\n")
    

        # if 1600 < x < 1800 and 2 < y < 33:
        #     pg.click()#左键单击
        # if 1400 < x < 1370 and 600 < y < 620:
        #     pg.click(button='right')#右键单击
        # if 1600 < x < 1800 and 5 < y < 63:
        #     pg.doubleClick()#左键双击
        
# pg.click(400, 400)
# pg.typewrite('Hello world!', 0.25)

while 1:
    pg.moveTo(random.randint(0,1919),random.randint(0,1079),duration=1)
    time.sleep(2)

# https://blog.csdn.net/Romantic_wennuan/article/details/127181034