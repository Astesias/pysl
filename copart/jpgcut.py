from PIL import Image as i
import time
import sys

def filename2end(path,point=True):
    if type(path)!=type('str'):
        raise TypeError('path is a str,not {}'.format(type(path)))
    if point:
        return path[path.rfind('.'):]
    else:
        return path[path.rfind('.')+1:]

ipath=r'D:\Desktop\temp\j.png'
opath=r'D:\Desktop\temp/'
form=filename2end(ipath)

time.sleep(2)
a=i.open(ipath)
print(a)
wid=a.width
hei=a.height

hang=int(input('列|数:'))
lie=int(input('行——数:'))
print('\nstart')
box1=[0,0,wid/hang,hei/lie]#左 上 右 下
box=[0,0,wid/hang,hei/lie]
c=1

for j in range(lie):
    for k in range(hang):
        #print(box)
        b=a.crop(box)
        box[0]+=wid/hang
        box[2]+=wid/hang
        b.save(opath+'{}{}.{}'.format(j+1,k+1,form))
        sys.stdout.flush()
        print('\r进度'+str(c/hang/lie*100)+'%')
        sys.stdout.flush()
        #b.show()
        c+=1
    #print()
    box[0]=box1[0]
    box[2]=box1[2]
    box[1]+=hei/lie
    box[3]+=hei/lie
#b=a.crop(box)
#b.save('sample.jpg')

#a.show()
#a.save('new.jpg')
print('done')