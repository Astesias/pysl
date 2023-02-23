import paddle.fluid as fluid
from paddle.fluid import ParamAttr
import numpy as np
import paddle
np.set_printoptions(precision=2)

def main():         #使map变大 上采样方法.双线性插值法
    with fluid.dygraph.guard(fluid.CPUPlace()):
        data=np.array([[1,2],
                       [3,4]]).astype(np.float32)
        #data=np.array([[1,2,3],
                        # [3,4,5]
                        # [6,7,8]]).astype(np.float32)
                        
        data=data[None,np.newaxis,:,:] #reshape
        
        data=fluid.dygraph.to_variable(data)
        
        out=fluid.layers.interpolate(data,out_shape=(4,4),align_corners=True)
        
        out=out.numpy()
        
        print(out.squeeze((0,1)))
        
if __name__ == '__main__':
    main()