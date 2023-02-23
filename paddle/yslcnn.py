import paddle
import numpy as np
from paddle.fluid.dygraph import Conv2D,Pool2D,Conv2DTranspose,to_variable
from paddle.nn import Layer
from paddle.fluid.layers import fc,softmax




class YslNet(Layer):        # input 3*224*224
    def __init__(self,num_classes=12):
        
        super(YslNet, self).__init__()
        
        self.num_classes=num_classes
        
        self.conv1=Conv2D(3,64,filter_size=2,stride=1)                  #64*224*224
        self.pool1=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)     #64*122*122
        
        self.conv21=Conv2D(64,128,filter_size=2,stride=1)                #128*122*122
        self.conv22=Conv2D(64,128,filter_size=2,stride=1,padding=100)  
        self.pool2=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)     #128*56*56
        
        self.conv3=Conv2D(128,256,filter_size=2,stride=1)               #256*56*56
        self.pool3=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)     #256*28*28       
        
        self.conv4=Conv2D(256,512,filter_size=2,stride=1)               #512*28*28
        self.pool4=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)     #512*14*14     

        self.pool5=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)     #512*7*7      
        
        
        
    def forward(self,inputs):
        x = self.conv1(inputs)
        x = self.pool1(x)
        
        if(x.shape[2] <= 100 or x.shape[3] <= 100 ):
            x = self.conv22(x)
        else:
            x = self.conv21(x)
        x = self.pool2(x)
        
        x = self.conv3(x)
        x = self.pool3(x)

        x = self.conv4(x)
        x = self.pool4(x) 

        x = self.pool5(x) 
        
        x = fc(x,self.num_classes,act='softmax')
        
        return x
    
    
    
b=YslNet(num_classes=12)    
print(0)
x= np.random.rand(1,3,2,2).astype(np.float32)
x=to_variable(x) 
print(x.shape)

b(x)
    
    
    
    
    
    
    
    
        