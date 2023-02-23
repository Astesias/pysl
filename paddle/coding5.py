import numpy as np
import paddle.fluid as fluid
from paddle.fluid.dygraph import to_variable
from paddle.fluid.dygraph import Conv2D
from paddle.fluid.dygraph import Conv2DTranspose
from paddle.fluid.dygraph import Dropout
from paddle.fluid.dygraph import BatchNorm
from paddle.fluid.dygraph import Pool2D
from paddle.fluid.dygraph import Linear

from vgg16ysl import VGG16 #...
class FCN8s(fluid.dygraph.Layer):
    def __init__(self,num_classes=59):
        super(FCN8s,self).__init__()
        backbone=VGG16(pretrained=False)
        
        self.layer1=backbone.layer1
        #self.layer1[0].conv._padding=100
        self.pool1=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)
        
        self.layer2=backbone.layer2
        self.pool2=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)
        
        self.layer3=backbone.layer3
        self.pool3=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)
        
        self.layer4=backbone.layer4
        self.pool4=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)
        
        self.layer5=backbone.layer5
        self.pool5=Pool2D(pool_size=2,pool_stride=2,ceil_mode=True)
        
        self.fc6=Conv2D(512,4096,7,act='relu')     
        self.fc7=Conv2D(4096,4096,1,act='relu')
        
        self.drop6=Dropout()
        self.drop7=Dropout()
    
        self.score=Conv2D(4096,num_classes,1)
        self.score_pool3=Conv2D(256,num_classes,1)
        self.score_pool4=Conv2D(512,num_classes,1)
        
        self.up_output=Conv2DTranspose(num_channels=num_classes,
                                        num_filters=num_classes,
                                        filter_size=4,
                                        stride=2,
                                      # padding=1,
                                        bias_attr=False)
        
        self.up_output4=Conv2DTranspose(num_channels=num_classes,
                                        num_filters=num_classes,
                                        filter_size=4,
                                        stride=2,
                                        bias_attr=False)
        
        self.up_final=Conv2DTranspose(num_channels=num_classes,
                                        num_filters=num_classes,
                                        filter_size=16,
                                        stride=8,
                                        bias_attr=False)
        
        
        
        
        
    def forward(self,inputs):
        print(inputs.shape,'1')
        x=self.layer1(inputs)    #conv
        print(x.shape,'2')
        x=self.pool1(x)#1/2       pooling
        print(x.shape,'3')
        x=self.layer2(x)
        print(x.shape,'4')
        x=self.pool2(x)#1/4
        print(x.shape,'5')
        x=self.layer3(x)
        print(x.shape,'6')
        x=self.pool3(x)#1/8
        pool3=x                 #记录三层数据 up-pooling用
        print(x.shape,'7')
        x=self.layer4(x)
        print(x.shape,'8')
        x=self.pool4(x)#1/16
        pool4=x
        print(x.shape,'9')
        x=self.layer5(x)
        print(x.shape,'10')
        x=self.pool5(x)#1/32
        
        print(x.shape,'11')
        x=self.fc6(x)
        x=self.drop6(x)
        print(x.shape,'11')
        x=self.fc7(x)
        x=self.drop7(x)
        print(x.shape,'12')
        x=self.score(x)
        x=self.up_output(x)
        print(x.shape,'13')
        up_output=x #1/16
        x=self.score_pool4(pool4)
        print(x.shape,'14')
        
        x=x[:,:,5:5+up_output.shape[2],5:5+up_output.shape[3]]
        print(x.shape,'15')
        up_pool4=x
        x=up_pool4+up_output
        print(x.shape,'16')
        x=self.up_output4(x)
        print(x.shape,'17')
        up_pool4=x
        
        x=self.score_pool3(pool3)
        print(x.shape,'18')
        x=x[:,:,9:9+up_output.shape[2],9:9+up_output.shape[3]]
        print(x.shape,'19')
        up_pool3=x #1/8
        
        x=up_pool3+up_pool4
        print(x.shape,'20')
        x=self.up_final(x)
        print(x.shape,'21')
        x=x[:,:,31:31+inputs.shape[2],31:31+inputs.shape[3]]
        print(x.shape,'22')
             
        return x
      
        
def main():
    place=fluid.CPUPlace()
    with fluid.dygraph.guard(place):
        x_data=np.random.rand(2,3,512,512).astype(np.float32)
        x=to_variable(x_data)
        model=FCN8s(num_classes=59)
        model.eval()
        pred=model(x)
        print(pred.shape)

if __name__ == '__main__':
    main()