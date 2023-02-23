from tkinter import*
import random
box=Tk(screenName='hhhh')
box.title('界面')
box.geometry('600x600')
list=Listbox(width=500,height=500,font=("Helvetica",20),foreground=("blue"))
for i in range(10):  
      list.insert(0,random.randint(1,1000))
list.pack()
box.mainloop()










# root = Tk()                     # 创建窗口对象的背景色
#                                 # 创建两个列表
# li     = ['C','python','php','html','SQL','java']
# movie  = ['CSS','jQuery','Bootstrap']
# listb  = Listbox(root)          #  创建两个列表组件
# listb2 = Listbox(root)
# for item in li:                 # 第一个小部件插入数据
#     listb.insert(0,item)
 
# for item in movie:              # 第二个小部件插入数据
#     listb2.insert(0,item)
 
# listb.pack()                    # 将小部件放置到主窗口中
# listb2.pack()
# root.mainloop()                 # 进入消息循环