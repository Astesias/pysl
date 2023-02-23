import paddle
import paddle.fluid as fluid
from paddle.fluid.dygraph import to_variable  #使numpy对象可使用
from paddle.fluid.dygraph import Conv2D   #构建一个二维卷积层
from paddle.fluid.dygraph import Pool2D   #为二维空间池化操作
import numpy as np
np.set_printoptions(precision=1) #浮点数精确度

class BasicModel(fluid.dygraph.Layer):
    def __init__(self,num_classes=59):
        super(BasicModel, self).__init__()
        self.pool=Pool2D(pool_size=2,pool_stride=2) #池化核大小 池化步长
        self.conv=Conv2D(num_channels=3,num_filters=num_classes,filter_size=1) #滤波器个数 滤波器大小默认1*1
        
    def forward(self,inputs):
        x=self.pool(inputs)
        x=fluid.layers.interpolate(x,out_shape=inputs.shape[2::])  #用于调整一个batch中图片的大小
        x=self.conv(x)
        
        return x

def main():
    place=paddle.fluid.CPUPlace()
    #CUDA
    with fluid.dygraph.guard(place):    #context
        model=BasicModel(num_classes=59)
        model.eval() #train  父类的预测模式
        input_data=np.random.randn(1,3,8,8,).astype(np.float32) #b c 8*8
        print('input data shape:\n',input_data.shape)
        print(input_data)
        input_data=to_variable(input_data)
        print(input_data)
        output_data=model(input_data)
        
        output_data=output_data.numpy()
        print('\n\n\n\n',output_data)
        print('output data shape:\n',output_data.shape)
        
        
        
if __name__ == '__main__':
    main()