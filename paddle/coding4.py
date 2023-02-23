import paddle.fluid as fluid
from paddle.fluid import ParamAttr
import numpy as np
np.set_printoptions(precision=2)

def main():  #
    with fluid.dygraph.guard(fluid.CPUPlace()):
        data=np.array([[1,2],
                       [3,4]]).astype(np.float32)
        #data=np.array([[1,2,3],
                        # [3,4,5]
                        # [6,7,8]]).astype(np.float32)
                        
        data=data[np.newaxis,np.newaxis,:,:] #reshape
        
        data=fluid.dygraph.to_variable(data)
        
        convw=np.array([[1,2,3],
                        [4,5,6],
                        [7,8,9]]).astype(np.float32)   #filter
        
        print(convw)
        convw=convw[np.newaxis,np.newaxis,:,:]
        
        w_init=fluid.initializer.NumpyArrayInitializer(convw)   #初始化参数变量
        param_attr=fluid.ParamAttr(initializer=w_init)
        conv_t=fluid.dygraph.Conv2DTranspose(num_channels=1,
                                             num_filters=1,
                                             filter_size=3,
                                             padding=0,
                                             stride=1,
                                             param_attr=param_attr          #预设卷积核
                                             )
        
        out=conv_t(data)
        out=out.numpy()
        
        print(out.squeeze((0,1)))
        
if __name__ == '__main__':
    main()