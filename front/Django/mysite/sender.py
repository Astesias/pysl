import json,time
from pysl import random_name,cmd
from threading import Thread as thd
from manage import main

def write():
    while 1:
        time.sleep(1)
        with open('tmp.json','w') as fp:
            json.dump(
                {'msg':random_name(5)},
                fp
            )

if __name__=='__main__': 
    thd(target=write).start()
    main()
