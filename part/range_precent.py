import time
import sys
import threading





class range_precent():
    def __init__(self,total):
        self.total = total
    def update(self,now,obj="█",nonobj='░',process_name='进度'):
        precent=now/self.total
        num=int(100*precent)
        sys.stdout.flush()

        print("\r\r\r", end="")
        print("{} {:>3}% |".format(process_name,num),obj*(num//3),nonobj*(33-num//3),'|{}/{}'.format(now,self.total),sep='', end="")
        sys.stdout.flush()

a=range_precent(100)

for i in range(101):
    a.update(i)
    time.sleep(0.01)


