import paddle
import paddle.fluid as fluid
from paddle.nn import Conv2D, BatchNorm2D, LeakyReLU, MaxPool2D, LSTM, Linear, Dropout
from paddle.io import Dataset
import os
import cv2
import numpy as np
from paddle.vision.transforms import Compose, Resize
from paddle.vision.models import ResNet, resnet34,resnet101
from paddle.fluid.dygraph import Layer
from paddle.fluid.dygraph import Conv2D
from paddle.fluid.dygraph import BatchNorm
from paddle.fluid.dygraph import Pool2D
from paddle.fluid.dygraph import Conv2DTranspose
from paddle.fluid.layers import fc,softmax


class Encoderf(Layer):
    def __init__(self, num_channels, num_filters):
        super(Encoderf, self).__init__()
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


class Decoderf(Layer):
    def __init__(self, num_channels, num_filters):
        super(Decoderf, self).__init__()
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
    def __init__(self, num_classes=12):
        super(UNet, self).__init__()
        # encoder: 3->64->128->256->512
        self.down1 = Encoderf(num_channels=3, num_filters=64)
        self.down2 = Encoderf(num_channels=64, num_filters=128)
        self.down3 = Encoderf(num_channels=128, num_filters=256)
        self.down4 = Encoderf(num_channels=256, num_filters=512)

        # mid: 512->1024->1024
        self.mid_conv1 = Conv2D(512, 1024,1)
        self.mid_bn1 = BatchNorm(1024, act='relu')
        self.mid_conv2 = Conv2D(1024, 1024,1)
        self.mid_bn2 = BatchNorm(1024, act='relu')
        
        #TODO: 4 encoders, 4 decoders, and mid layers contains 2 1x1conv+bn+relu
        self.up4 = Decoderf(1024, 512)
        self.up3 = Decoderf(512, 256)
        self.up2 = Decoderf(256, 128)
        self.up1 = Decoderf(128, 64)

        self.last_conv = Conv2D(64, num_classes, 1)


    def forward(self, inputs):
        x1, x = self.down1(inputs)
        print(x1.shape, x.shape,'x1')
        x2, x = self.down2(x)
        print(x2.shape, x.shape,'x2')
        x3, x = self.down3(x)
        print(x3.shape, x.shape,'x3')
        x4, x = self.down4(x)
        print(x4.shape, x.shape,'x4')

        # middle layers
        x = self.mid_conv1(x)
        x = self.mid_bn1(x)
        x = self.mid_conv2(x)
        x = self.mid_bn2(x)

        print(x4.shape, x.shape,'ux4')
        x = self.up4(x4, x)
        print(x3.shape, x.shape,'ux3')
        x = self.up3(x3, x)
        print(x2.shape, x.shape,'ux2')
        x = self.up2(x2, x)
        print(x1.shape, x.shape,'ux1')
        x = self.up1(x1, x)
        print(x.shape,'ux4')
        
        x = self.last_conv(x)
        
        x = paddle.tensor.flatten(x, 1)
        print(x.shape)

        return x

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







##########################################################
class Reader(Dataset):                                   #
    """
    步骤一：继承paddle.io.Dataset类
    """
    def __init__(self, data):         #data:  ([d,l],[d,l],[d,l])
        """
        步骤二：实现构造函数，定义数据集大小
        """
        super().__init__()
        self.samples = data

    def __getitem__(self, index):     #a=Reader(Dataset)   a[index]
        """
        步骤三：实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据，对应的标签）
        """
        # 处理图像
        img_name = self.samples[index][0].split('/')[1]    
        img_path = os.path.join(cfg["train_path"], img_name)
        img = cv2.imread(img_path)              # h w 3
        #print(img.shape,img_path)
        img = cv2.resize(img,(48,256)) #灰度处理preprocess(img)     #  (3, 48, 256)

        # 处理标签
        label = self.samples[index][1]           
        label = paddle.to_tensor(np.int64(label))   #变为可操作对象
        
        
        #    img(w,b)->label(y)
        
        return img, label    #第index张图片的灰度数据与标签

    def __len__(self):
        """
        步骤四：实现__len__方法，返回数据集总数目
        """
        return len(self.samples)                         #
##########################################################



##########################################################
class Net(paddle.nn.Layer):                              #定义网络   优化
    def __init__(self):
        super(Net, self).__init__()
        self.resnet = resnet101(True, num_classes=-1, with_pool=False)
        self.linear = Linear(32768, cfg["classify_num"])   #输入/出层数   4096:12

    def forward(self, x):
        # (-1, 3, 48, 256)
        x = self.resnet(x)
        # (-1, 512, 2, 8)
        print(x.shape)
        x = paddle.tensor.flatten(x, 1)   #展平维度
        # (-1, 512x2x8)
        x = self.linear(x)  #return self._dygraph_call_func(*inputs, **kwargs)
        print(x.shape)
        return x                                         #
##########################################################


##########################################################
class InferReader(Dataset):                              #
    """
    步骤一：继承paddle.io.Dataset类
    """
    def __init__(self, data):
        """
        步骤二：实现构造函数，定义数据集大小
        """
        super().__init__()
        self.samples = data

    def __getitem__(self, index):
        """
        步骤三：实现__getitem__方法，定义指定index时如何获取数据，并返回单条数据（训练数据，对应的标签）
        """
        # 空图片返回xxx
        if self.samples[index][1] == False:
            return np.zeros(3*48*256).reshape((3, 48, 256)).astype(np.float32)
        transform = Compose([
            Resize(size=(48, 256)),
        ])
        img = transform(cv2.imread(os.path.join(cfg['test_path'], self.samples[index][0]))).reshape((3, 48, 256)).astype('float32')
        return img / 255.

    def __len__(self):
        """
        步骤四：实现__len__方法，返回数据集总数目
        """
        return len(self.samples)                         #
##########################################################

    
def preprocess(img):
    transform = Compose([
        Resize((48, 256)),     
        ])
    
    img = transform(img).reshape(cfg["input_size"]).astype("float32")   # (3, 48, 256)
    print(img.shape,'img')
    return img / 255.        #归一化
        

def cv2_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    #cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img


        
def creat_filp_pic(cfg):
    train_data = list()
    with open(cfg["train_list"], "r") as f:              #打开 训练路径\t答案 文件
        for line in f:         
            name, label = line.strip().split('\t')       # cat_12_train/WORaDysJBKwiYtQ0M8TugcfjE6PAmnzZ.jpg 10
            if (cv2_imread(os.path.join(cfg['train_path'], name.split('/')[1])) is not None):   #若成功读取
                train_data.append([name, label]) 
    pathss=[]
    for path,result in train_data:
        file = cv2_imread(path)
        new_file = cv2.flip(file, -1)
        k=path.index('/')+1
        newpath = path[:k] + 'new_' + path[k:]
        pathss.append((newpath,result))
        if new_file is not None:
            cv2.imwrite(newpath,new_file)
        else:
            print('a pic is failed to load')
    fp=open(cfg["train_list"],'a')
    for path,label in pathss:
        a = '\n' + str(path) + '\t' + str(label)
        fp.write(a)
    fp.close()
    print('done')
        
        
        
        
        
cfg = {                                       #设置路径和参数
    "epoch": 10,
    "batch_size": 32,  #32一组 68小轮
    "input_size": (3, 48, 256),
    "classify_num": 12,
    "learning_rate": 1e-3,

    "train_list": "./test.txt",   #./train_list.txt
    "test_list": "./test_list.txt",
    "train_path": "./cat12train",   #./cat_12_train
    "test_path": "./cat_12_test",
    
    "pic_filp":False
}   


if(cfg["pic_filp"]):
    creat_filp_pic(cfg)

train_data = list()
with open(cfg["train_list"], "r") as f:              #打开 训练路径\t答案 文件
    for line in f:         
        name, label = line.strip().split('\t')       # cat_12_train/WORaDysJBKwiYtQ0M8TugcfjE6PAmnzZ.jpg 10
        if (cv2.imread(os.path.join(cfg['train_path'], name.split('/')[1])) is not None):   #若成功读取
            train_data.append([name, label]) 



train_loader = paddle.io.DataLoader(Reader(train_data), batch_size=cfg["batch_size"], shuffle=True) #False and use seed  
#读入数据 设置批次 打乱


        
        

# 定义输入层，shape中第0维使用-1则可以在推理时自由调节batch size  
input_define = paddle.static.InputSpec(
    shape=[-1, cfg["input_size"][0], cfg["input_size"][1], cfg["input_size"][2]],
    dtype="float32",
    name="img")
        


# 定义标签
label_define = paddle.static.InputSpec(
    shape=[-1, cfg["classify_num"]],
    dtype="int32",
    name="label")

# 实例化模型
model = paddle.Model(UNet(), inputs=input_define, labels=label_define) #(-1,3,48,256) (-1,12)

model.summary()

# 定义优化器
optimizer = paddle.optimizer.Adam(learning_rate=cfg["learning_rate"], parameters=model.parameters())

# 为模型配置运行环境并设置该优化策略
model.prepare(
    optimizer=optimizer,          #优化器策略
    loss=paddle.nn.CrossEntropyLoss()   #loss策略
    )

# 执行训练
model.fit(
    # no train_loader()
    train_data= train_loader,
    batch_size=cfg["batch_size"],
    epochs=cfg["epoch"],
    verbose=1,  #进度条日志
    )
#可加eval_data进行评估


test_data = list()
for img_name in os.listdir(cfg['test_path']):   #contain [····'jcBJ5x2h9ASa7N1p0GdKsmPQFobW8v4e.jpg'····]

    if (cv2.imread( os.path.join( cfg['test_path'], img_name ) )) is not None: # './cat_12_test'
        
        test_data.append([img_name, True])
    else:
        test_data.append([img_name, False])   #判断test是否可用
        
        
test_loader = paddle.io.DataLoader(InferReader(test_data))   #迭代器 相当于在data后增加[n]

res = model.predict(test_loader)    #arrar([12],[12],[12],[12]) 12类猫的概率 取最大值的索引作为结果
with open(r'.\result.csv', 'w') as f:
    for i in range(240):
        f.write(test_data[i][0] + ',' + str(np.argmax(np.array(res[0][i]))) + '\n')
        
        
