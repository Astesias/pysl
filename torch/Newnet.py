import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torch.utils.data as data
import cv2
import PIL
from pysl import cv2_imread
import numpy as np

def s(x):
    print(type(x),x.shape)
    
def tenor2img(tensor):
    if type(tensor)== type(torch.zeros(1)):      
        try:
            n,a,b,c=tensor.shape
     
        except:
            a,b,c=tensor.shape
        if a<b:
            tensor=tensor.reshape(b,c,a)
        if tensor.mean()>1:
            tensor=np.array(tensor.detach(),dtype=np.uint8)
        else:
            tensor=np.array(tensor.detach())
            
 
        
    # s(tensor)
    # print(tensor)
    try:
        cv2.imshow('n',tensor)
    except:
        cv2.imshow('w',tensor[:,:,0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    

class Mynet(nn.Module):
    def __init__(self):
        super(Mynet,self).__init__()
 
        self.transforms=transforms.Compose([
                                    transforms.ToTensor(),
                                    transforms.Resize(1,3,1024,1024)
                                    
                               ])
        
    
        self.layer1=nn.Sequential(nn.Conv2d(3,64,3,padding=1),
                               nn.MaxPool2d(2),
                               nn.BatchNorm2d(64),
                               nn.ReLU()
                               )
        
        self.layer2=nn.Sequential(nn.Conv2d(64,128,3,padding=1),
                       nn.MaxPool2d(2),
                       nn.BatchNorm2d(128),
                       nn.ReLU()
                       )
        
        self.layer3=nn.Sequential(
                        nn.Conv2d(3,3,3,padding=1),
                        # nn.MaxPool2d(2),
                        nn.BatchNorm2d(3),
                        # nn.ReLU()
                       )
    def trans(self,x):
        return  torch.tensor(x).reshape(1,3,1024,1024).float()
        
    def forward(self,x):
        
        tenor2img(x)
        x=self.trans(x)

        # y=x.clone()
         
        
        # x=self.layer1(x)  
        # tenor2img(x)
        # x=self.layer2(x)  
        
        
        
        x=self.layer3(x)
  
        tenor2img(x)
  
 
        return x
    

net=Mynet()

x=cv2_imread(r'D:\Desktop\.py\datas\jpg.jpg')  

# x=torch.tensor(img).reshape(1,3,1024,1024).float()

# img=PIL.Image.open(r'D:\Desktop\.py\datas\jpg.jpg')

x=net(x)





    