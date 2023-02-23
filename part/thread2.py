import psutil
for q in psutil.pids():
    p=psutil.Process(q)
    print(p)
    #if 'Nemu' in str(p):
        #p.kill()

