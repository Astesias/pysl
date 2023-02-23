import os
import random
import numpy as np
import cv2
import paddle.fluid as fluid
####
class Transform(object):        #map变小
    def __init__(self,size=256):
        self.size=size
    def __call__(self,inputs,label):
        inputs=cv2.resize(inputs,(self.size,self.size),interpolation=cv2.INTER_LINEAR)
        #          需要改变尺寸的图像 目标图像大小     插值方法(最近邻插值法↓ 双线性插值法↑)
        label=cv2.resize(inputs,(self.size,self.size),interpolation=cv2.INTER_NEAREST)
        
        return inputs,label
        
class BasicDataLoader(object):
    def __init__(self,
                 image_folder,
                 image_list_file,
                 transform=None,
                 shuffle=True):
        self.image_folder=image_folder
        self.image_list_file=image_list_file
        self.transform=transform
        
        self.shuffle=shuffle
        self.data_list=self.read_list()
        
    def read_list(self):
        data_list=[]
        with open(self.image_list_file) as infile:
            for line in infile:
                print(line)
                # data_path=os.path.join(self.image_folder,line.split()[0]) #图像地址在前      
                # label_path=os.path.join(self,self.image_folder,line.split()[1])  #结果地址在后  
                data_path=line.split()[0] #图像地址在前      
                label_path=line.split()[1]  #结果地址在后  
                data_list.append((data_path,label_path)) #(图像地址，结果地址)
        
        #@if(self.shuffle):
                random.shuffle(data_list) #打乱一维元素
        return data_list
           
    def preprocess(self,data,label):
        h,w,c=data.shape  #hight wight color
        h_gt,w_gt=label.shape #灰度图只有两个参数
        assert h==h_gt, 'error'  #相当于if no: print
        assert w==w_gt, 'error'
        
        if self.transform:
            data,label=self.transform(data,label)  #调用__call__()使用自定义的变换方法
        label=label[:,:, np.newaxis]   #增加新维度np.array([1,2,3,4,5]) -> np.array([[1],[2],[3],[4],[5]])
        return data,label
  
        
    def __len__(self):
        
        return len(self.data_list)

        
    def __call__(self):
        for data_path,label_path in self.data_list:   #取出地址
            data=cv2.imread(data_path)        #读取图片
            print(data.shape,'$$$')
            data=cv2.cvtColor(data,cv2.COLOR_BGR2RGB) #bgr to rbg
            print(data.shape,'***')
            label=cv2.imread(label_path,cv2.IMREAD_GRAYSCALE)   #以灰度图打开
            print(data.shape,label.shape)           #显示维度
            data,label=self.preprocess(data,label)
            yield data,label

def main():
    batch_size=1 #批次 5
    place=fluid.CPUPlace() #cpu环境
    with fluid.dygraph.guard(place):#with结构中打开文件
        transform=Transform(256)    #对图像进行变换
        basic_dataloader=BasicDataLoader(
            image_folder=r'C:\Users\ysl\Desktop\technologicalinnovation\imagejudge\dataset\humanseg', #文件路径 不能有中文
            image_list_file=r'C:\Users\ysl\Desktop\technologicalinnovation\imagejudge\dataset\humanseg\list.txt', #文件列表
            transform=transform,    
            shuffle=True   #打乱
            )
        dataloader=fluid.io.DataLoader.from_generator(capacity=1,use_multiprocess=False)
        dataloader.set_sample_generator(basic_dataloader,  #自定义的读取方式内部调用__call__())
                                        batch_size=batch_size,
                                        places=place)   #以上两句固定格式
    
        #dataloader此时为处理完成的图片
        #形式为[ ([array data1],[array label1]) ([array data2],[array label2]) ([array data3],[array label3]) ···]
        
    num_epoch=2
    for epoch in range(1,num_epoch+1):
        print(f'Epoch [{epoch}/{num_epoch}]:')   #格式化字符串常量
        for idx,(data,label) in enumerate(dataloader):
            print(f'Iter {idx}\nData shape: {data.shape}\nLabel shape: {label.shape}\n')    #[n,h,w,c]
            
     
if __name__ == '__main__':
        main()

