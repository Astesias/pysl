import numpy as np
import matplotlib.pyplot as plt
class Network(object):
  def __init__(self,num_of_weights):
      np.random.seed(0)
      self.w = np.random.randn(num_of_weights,1)
      self.b = 0
  def forward(self,x):
      z = np.dot(x,self.w) + self.b
      return z
  def loss(self,z,y):
      error = z - y
      cost = error * error
      cost = np.mean(cost)
      return cost
  def gradient(self,x,y):
      z = self.forward(x)
      g_w = (z-y)*x
      g_w = np.mean(g_w,axis=0)
      g_w = g_w[:,np.newaxis]
      g_b = (z-y)
      g_b = np.mean(g_b)
      
      return g_w,g_b
  def update(self,g_w,g_b,eta=0.01):
      self.w=self.w-eta*g_w
      self.b=self.b-eta*g_b
  def train(self,training_data,num_epoches,batch_size=10,eta=0.01):
      losses=[]
      n=len(training_data)
      for epoch_id in range(num_epoches):
          np.random.shuffle(training_data)
          mini_batches = [train_data[k:k+batch_size] 
                          for k in range(0,n,batch_size)]
          for iter_id,mini_batch in enumerate(mini_batches):
              x = mini_batch[:,:-1]
              y = mini_batch[:,-1:]   
              a = self.forward(x)
              loss = self.loss(a,y)
              g_w,g_b, = self.gradient(x,y)
              self.update(g_w,g_b,eta)
              losses.append(loss)
              print('Epoch {:3d}/iter {:3d},loss = {:.4f}'.
                    format(epoch_id,iter_id,loss))
      return losses
  
  # def train(self,x,y,iterations=100,eta=0.01):
  #     losses=[]
  #     for i in range(iterations):
  #         z=self.forward(x)
  #         L=self.loss(z,y)
  #         g_w,g_b,=self.gradient(x,y)
  #         self.update(g_w,g_b,eta)
  #         losses.append(L)
  #         if(i+1)%10 == 0:
  #             print('iter {},loss {}'.format(i,L))
  #     return losses
    
    
    
    
    
    
def load_data():
    # 从文件导入数据
    datafile = r'D:\360极速浏览器下载\housing.data'
    data = np.fromfile(datafile, sep=' ', dtype=np.float32)

    # 每条数据包括14项，其中前面13项是影响因素，第14项是相应的房屋价格中位数
    feature_names = [ 'CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', \
                      'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT', 'MEDV' ]
    feature_num = len(feature_names)

    # 将原始数据进行Reshape，变成[N, 14]这样的形状
    data = data.reshape([data.shape[0] // feature_num, feature_num])

    # 将原数据集拆分成训练集和测试集
    # 这里使用80%的数据做训练，20%的数据做测试
    # 测试集和训练集必须是没有交集的
    ratio = 0.8
    offset = int(data.shape[0] * ratio)
    training_data = data[:offset]

    # 计算train数据集的最大值，最小值，平均值
    maximums, minimums, avgs = training_data.max(axis=0), training_data.min(axis=0), \
                                 training_data.sum(axis=0) / training_data.shape[0]
    
    # 记录数据的归一化参数，在预测时对数据做归一化
    global max_values
    global min_values
    global avg_values
    max_values = maximums
    min_values = minimums
    avg_values = avgs

    # 对数据进行归一化处理
    for i in range(feature_num):
        data[:, i] = (data[:, i] - avgs[i]) / (maximums[i] - minimums[i])

    # 训练集和测试集的划分比例
    training_data = data[:offset]
    test_data = data[offset:]
    return training_data, test_data

# #获取数据
# train_data,test_data = load_data()
# x = train_data[:,:-1]
# y = train_data[:,-1:]
# #创建网络
# net = Network(13)
# num_iterations=2000
# #启动训练
# losses = net.train(x, y,iterations=num_iterations,eta=0.01)
# #画出损失函数的变化趋势
# plot_x = np.arange(num_iterations)
# plot_y = np.array(losses)
# plt.plot(plot_x,plot_y)
# plt.show()

#获取数据
train_data,test_data = load_data()

#打乱样本顺序
np.random.shuffle(train_data)

#分解为多段
batch_size = 10
n = len(train_data)
min_batches = [train_data[k:k+batch_size] for k in range(0,n,batch_size)]
   
#创建网络
net = Network(13)
num_iterations=2000

#启动训练

losses = net.train(train_data,num_epoches=50,batch_size=100,eta=0.1)

#画出损失函数的变化趋势
plot_x = np.arange(len(losses))
plot_y = np.array(losses)
plt.plot(plot_x,plot_y)
plt.show()

print(net.w,net.b)

