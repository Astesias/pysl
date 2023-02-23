import paddle
import numpy as np
from paddle.fluid.dygraph import Conv2D,Pool2D,Conv2DTranspose,to_variable,BatchNorm,Dropout
from paddle.nn import Layer
from paddle.fluid.layers import fc


# class resnet34(Layer):
#     def __init__(self,num_channels,num_filters):
#         super(resnet34,self).__init()
        
class YslNet(Layer):        # input 3*224*224
    def __init__(self,num_classes=12):
        
        super(YslNet, self).__init__()
        
        self.num_classes=num_classes
        
        self.conv0=Conv2D(3,64,filter_size=7,stride=2,padding=3)            #64*122*122
        self.pool0=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)         #64*122*122

        self.conv1=Conv2D(64,64,filter_size=7,stride=1,padding=3) 
        
        self.conv21=Conv2D(64,128,filter_size=1,stride=2,padding=0)
        self.conv22=Conv2D(64,128,filter_size=7,stride=2,padding=3)
        self.conv23=Conv2D(128,128,filter_size=7,stride=1,padding=3)
        
        self.conv31=Conv2D(128,256,filter_size=1,stride=2,padding=0)
        self.conv32=Conv2D(128,256,filter_size=7,stride=2,padding=3)
        self.conv33=Conv2D(256,256,filter_size=7,stride=1,padding=3)
        
        self.conv41=Conv2D(256,512,filter_size=1,stride=2,padding=0)
        self.conv42=Conv2D(256,512,filter_size=7,stride=2,padding=3)
        self.conv43=Conv2D(512,512,filter_size=7,stride=1,padding=3)
        
        self.pool5=Pool2D(pool_size=2,pool_type='avg',pool_stride=2,ceil_mode=True)
        
        self.drop=Dropout()
        self.bn1=BatchNorm(64,act='tanh')
        self.bn2=BatchNorm(128,act='tanh')
        self.bn3=BatchNorm(256,act='tanh')
        self.bn4=BatchNorm(512,act='tanh')
        
    def layer1(self,inputs):
        
        concat1 = inputs
        inputs = self.conv1(inputs)
        inputs = self.conv1(inputs)
        inputs = concat1 + inputs
        concat2 = inputs
        
        inputs = self.conv1(inputs)
        inputs = self.conv1(inputs)
        inputs = concat2 + inputs
        concat3 = inputs
        
        inputs = self.conv1(inputs)
        inputs = self.conv1(inputs)
        inputs = concat3 + inputs
        
        return inputs

    def layer2(self,inputs):  
        
        concat1 = self.conv21(inputs) 
        
        inputs = self.conv22(inputs)
        inputs = self.conv23(inputs)
        inputs = concat1 + inputs
        
        concat2 = inputs
        inputs = self.conv23(inputs)
        inputs = self.conv23(inputs)
        inputs = concat2 + inputs        

        concat3 = inputs
        inputs = self.conv23(inputs)
        inputs = self.conv23(inputs)
        inputs = concat3 + inputs
        
        concat4 = inputs
        inputs = self.conv23(inputs)
        inputs = self.conv23(inputs)
        inputs = concat4 + inputs
        
        return inputs
    
    
    def layer3(self,inputs):  
        
        concat1 = self.conv31(inputs) 
        
        inputs = self.conv32(inputs)
        inputs = self.conv33(inputs)
        inputs = concat1 + inputs
        
        concat2 = inputs
        inputs = self.conv33(inputs)
        inputs = self.conv33(inputs)
        inputs = concat2 + inputs        

        concat3 = inputs
        inputs = self.conv33(inputs)
        inputs = self.conv33(inputs)
        inputs = concat3 + inputs
        
        concat4 = inputs
        inputs = self.conv33(inputs)
        inputs = self.conv33(inputs)
        inputs = concat4 + inputs
        
        concat5 = inputs
        inputs = self.conv33(inputs)
        inputs = self.conv33(inputs)
        inputs = concat5 + inputs
        
        concat6 = inputs
        inputs = self.conv33(inputs)
        inputs = self.conv33(inputs)
        inputs = concat6 + inputs
        
        return inputs   
       
        
    def layer4(self,inputs):  
        
        concat1 = self.conv41(inputs) 
        
        inputs = self.conv42(inputs)
        inputs = self.conv43(inputs)
        inputs = concat1 + inputs
        
        concat2 = inputs
        inputs = self.conv43(inputs)
        inputs = self.conv43(inputs)
        inputs = concat2 + inputs        

        concat3 = inputs
        inputs = self.conv43(inputs)
        inputs = self.conv43(inputs)
        inputs = concat3 + inputs
        
        return inputs  
    
              
    def forward(self,inputs):
        x = self.conv0(inputs)
        x = self.pool0(x)
        
        
        x = self.layer1(x)
        x = self.bn1(x)
        
        x = self.layer2(x)
        x = self.bn2(x)
        
        x = self.layer3(x)
        x = self.bn3(x)
        
        x = self.layer4(x)
        x = self.bn4(x)
        
        x = self.pool5(x)
        
        x = self.drop(x)

        x = fc(x,self.num_classes,act='softmax')
        return x
        
place=paddle.fluid.CPUPlace()
with paddle.fluid.dygraph.guard(place):
    b=YslNet(num_classes=12)    
    x= np.random.rand(1,3,256,256).astype(np.float32)
    x=to_variable(x) 
    print(x.shape,'input')
    a=b(x)
    print(a.shape,'output')
    

        


