import paddle
import numpy as np
from paddle.fluid.dygraph import Conv2D,Pool2D,to_variable,BatchNorm,Dropout
from paddle.nn import Layer
from paddle.fluid.layers import fc

class VGG16(Layer):
    def __init__(self,num_classes=1000,pretrained=False):   
        super(VGG16, self).__init__()
        self.classes=num_classes
        
        self.conv11=Conv2D(3,64,3,padding=1,act='relu')
        self.conv12=Conv2D(64,64,3,padding=1,act='relu')
        self.pool1=Pool2D(pool_size=2,pool_stride=2)
        
        self.conv21=Conv2D(64,128,3,padding=1,act='relu')
        self.conv22=Conv2D(128,128,3,padding=1,act='relu')
        self.pool2=Pool2D(pool_size=2,pool_stride=2)
        
        self.conv31=Conv2D(128,256,3,padding=1,act='relu')
        self.conv32=Conv2D(256,256,3,padding=1,act='relu')
        self.conv33=Conv2D(256,256,3,padding=1,act='relu')
        self.pool3=Pool2D(pool_size=2,pool_stride=2)
        
        self.conv41=Conv2D(256,512,3,padding=1,act='relu')
        self.conv42=Conv2D(512,512,3,padding=1,act='relu')
        self.conv43=Conv2D(512,512,3,padding=1,act='relu')
        self.pool4=Pool2D(pool_size=2,pool_stride=2)
        
        self.conv51=Conv2D(512,512,3,padding=1,act='relu')
        self.conv52=Conv2D(512,512,3,padding=1,act='relu')
        self.conv53=Conv2D(512,512,3,padding=1,act='relu')
        self.pool5=Pool2D(pool_size=2,pool_stride=2)     
        
        self.pool=Pool2D(pool_size=2,pool_stride=2) 
        
        self.fc5=Conv2D(512,4096,1,act='relu')  
        self.fc6=Conv2D(4096,4096,1,act='relu')  
        
        self.drop=Dropout()
        
        
    def layer1(self,inputs):
        x = self.conv11(inputs)
        x = self.conv12(x)

        
        return x
    
        
    def layer2(self,inputs):
        x = self.conv21(inputs)
        x = self.conv22(x)

        return x
        
    def layer3(self,inputs):
        x = self.conv31(inputs)
        x = self.conv32(x)
        x = self.conv33(x)

        
        return x
        
    def layer4(self,inputs):
        x = self.conv41(inputs)
        x = self.conv42(x)
        x = self.conv43(x)

        
        return x
        
    def layer5(self,inputs):
        x = self.conv51(inputs)
        x = self.conv52(x)
        x = self.conv53(x)

        
        return x
        
    def forward(self,inputs):
        
        x = self.layer1(inputs)
        x=self.pool(x)
        x = self.drop(x)
        
        # x = self.layer2(x)
        # x=self.pool(x)
        # x = self.drop(x)
        
        # x = self.layer3(x)
        # x=self.pool(x)
        # x = self.drop(x)
        
        # x = self.layer4(x)
        # x=self.pool(x)
        # x = self.drop(x)
        
        # x = self.layer5(x)
        # x=self.pool(x)
        # x = self.drop(x)
        
        # x = self.fc5(x)
        # x = self.fc6(x)
        
        # x = fc(x,self.classes,act='relu')
        
        return x
        
        
        
        
x = np.random.uniform(0,1,(1,3,224,224)).astype(np.float32)

x = to_variable(x)

with paddle.fluid.dygraph.guard():
    vgg=VGG16(num_classes=12)
    x = vgg(x)
    print(x.shape)
     
        
        
        
        
        
        
        
        
        