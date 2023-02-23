import numpy as np
import paddle
import paddle.fluid as fluid
from paddle.fluid.dygraph import to_variable
from paddle.fluid.dygraph import Layer
from paddle.fluid.dygraph import Conv2D
from paddle.fluid.dygraph import BatchNorm
from paddle.fluid.dygraph import Pool2D
from paddle.fluid.dygraph import Conv2DTranspose
import cv2
from paddle.vision.transforms import Compose, Resize

from paddle.nn import  Linear

np.set_printoptions(precision=10)

class Encoder(Layer):
    def __init__(self, num_channels, num_filters):
        super(Encoder, self).__init__()
        #TODO: encoder contains:
        #       1 3x3conv + 1bn + relu + 
        #       1 3x3conc + 1bn + relu +
        #       1 2x2 pool
        # return features before and after pool
        self.conv1 = Conv2D(num_channels,
                            num_filters,
                            filter_size=3,
                            stride=1,
                            padding=1)
        self.bn1 = BatchNorm(num_filters, act='relu')
        self.conv2 = Conv2D(num_filters,
                            num_filters,
                            filter_size=3,
                            stride=1,
                            padding=1)
        self.bn2 = BatchNorm(num_filters, act='relu')

        self.pooled = Pool2D(2, pool_type='max', pool_stride=2, ceil_mode=True)

    def forward(self, inputs):
        # TODO: finish inference part
        x = self.conv1(inputs)
        x = self.bn1(x)
        x = self.conv2(x)
        x = self.bn2(x)
        x_pooled = self.pooled(x)

        return x, x_pooled


class Decoder(Layer):
    def __init__(self, num_channels, num_filters):
        super(Decoder, self).__init__()
        # TODO: decoder contains:
        #       1 2x2 transpose conv (makes feature map 2x larger)
        #       1 3x3 conv + 1bn + 1relu + 
        #       1 3x3 conv + 1bn + 1relu
        self.up = Conv2DTranspose(num_channels,
                                num_filters,
                                filter_size=2,
                                stride=2,
                                )
        self.conv1 = Conv2D(num_channels,
                            num_filters,
                            filter_size=3,
                            stride=1,
                            padding=1)
        self.bn1 = BatchNorm(num_filters, act='relu')
        self.conv2 = Conv2D(num_filters,
                            num_filters,
                            filter_size=3,
                            stride=1,
                            padding=1)
        self.bn2 = BatchNorm(num_filters, act='relu')

    def forward(self, inputs_prev, inputs):

        # TODO: forward contains an Pad2d and Concat
        x = self.up(inputs)
        h_diff = inputs_prev.shape[2] - x.shape[2]
        w_diff = inputs_prev.shape[3] - x.shape[3]
        x = fluid.layers.pad2d(x, paddings=[h_diff//2, h_diff - h_diff//2, w_diff//2, w_diff - w_diff//2])
        
        x = fluid.layers.concat([inputs_prev, x], axis=1)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.conv2(x)
        x = self.bn2(x)

        #Pad

        return x


class UNet(Layer):
    def __init__(self, num_classes=59):
        super(UNet, self).__init__()
        # encoder: 3->64->128->256->512
        self.down1 = Encoder(num_channels=3, num_filters=64)
        self.down2 = Encoder(num_channels=64, num_filters=128)
        self.down3 = Encoder(num_channels=128, num_filters=256)
        self.down4 = Encoder(num_channels=256, num_filters=512)

        # mid: 512->1024->1024
        self.mid_conv1 = Conv2D(512, 1024,1)
        self.mid_bn1 = BatchNorm(1024, act='relu')
        self.mid_conv2 = Conv2D(1024, 1024,1)
        self.mid_bn2 = BatchNorm(1024, act='relu')
        
        #TODO: 4 encoders, 4 decoders, and mid layers contains 2 1x1conv+bn+relu
        self.up4 = Decoder(1024, 512)
        self.up3 = Decoder(512, 256)
        self.up2 = Decoder(256, 128)
        self.up1 = Decoder(128, 64)

        self.last_conv = Conv2D(64, num_classes, 1)
        self.linear = Linear(12*123*123, num_classes)


    def forward(self, inputs):
        x1, x = self.down1(inputs)
        x2, x = self.down2(x)
        x3, x = self.down3(x)
        x4, x = self.down4(x)

        # middle layers
        x = self.mid_conv1(x)
        x = self.mid_bn1(x)
        x = self.mid_conv2(x)
        x = self.mid_bn2(x)



        x = self.up4(x4, x)
        x = self.up3(x3, x)
        x = self.up2(x2, x)
        x = self.up1(x1, x)


        x = self.last_conv(x)
        
        
        # x = paddle.tensor.flatten(x, 1)
        # print(x.shape,'f')
        # x = self.linear(x)
        # print(x.shape,'l')

        return x


def cv2_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    #cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img

def preprocess(img):
    transform = Compose([
        Resize((256, 256)),     
        ])
    print(img.shape,'img')
    img = transform(img).reshape((3,256,256)).astype("float32")   # (3, 48, 256)
    print(img.shape,'img')
    return img / 255.    


def main():
    with fluid.dygraph.guard(fluid.CPUPlace()):
        model = UNet(num_classes=3)
     
        dir=r'C:\Users\ysl\Desktop\silk\backdata\298.png'
        a=cv2_imread(dir)
        print(a,'\n********')
        a=cv2.resize(a,(256,256),interpolation=cv2.INTER_NEAREST)

        a=to_variable(a)
        a=a.reshape((1,3,256,256))
        a=a/255
        p=model(a)
        p=p.reshape((256,256,3))
        
        p=p-p.min()
        p=p/p.max()
        
        
        p=p.numpy()*255
        p=p.astype(np.int)
        print(p)
        cv2.imshow('3',p)
        cv2.waitKey(0)
        
        
        
        
        
        
        
        # a=a[:,:,::-1].transpose((1,2,0))
        # b=b*255
        # b=b.numpy()
        # b=b.astype(np.int)
        # print(b)
        # cv2.imshow('4',b*255)
        # cv2.waitKey(0
        # pred = model(b))
        # print(b)
        # print('##################')
        # #print(pred,'\n\n\n\n\n\n')
        # print(pred.min())
        # #print(min(pred))
        # pred=pred.numpy()
        
        # pred=pred[0]
        # print(pred)
        # pred=pred[:,:,::-1].transpose((1,2,0))
        # print(pred.shape)
        # pred=pred-pred.min()
        # pred=pred/pred.max()*255
        # pred=pred.astype(np.int)
        # print(pred.shape)
        
        # cv2.imshow('3',pred)
        # cv2.waitKey(0)
        
        
        
        
        
if __name__ == "__main__":
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
