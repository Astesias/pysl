import os
import shutil
from pysl import getime,easytxt

copy_dict={
            r'D:\Desktop\.py':                              r'E:/copy_data/.py'  ,
            r'D:\Desktop\.c':                               r'E:/copy_data/.c'  ,
            r'D:\Desktop\.mat':                             r'E:/copy_data/.mat' ,
            r'D:\git\go-cqhttp_windows_amd64\code':         r'E:/copy_data/go-cqhttp',
            r'D:\Desktop\run\PaddleLiteDemo_1.8.1\Python':  r'E:/copy_data/baidu',
            # r'D:\Desktop\学习':r'E:/copy_data/学习'
            }

from_dir=list(copy_dict.keys())
for i in from_dir:  
    source_path = i
    target_path = copy_dict[i]
    if os.path.exists(copy_dict[i]):
        shutil.rmtree(copy_dict[i])
        print(copy_dict[i],'removed')
    try:
        shutil.copytree(source_path, target_path)
    except:
        print('{} to {} failed'.format(source_path, target_path))
    easytxt(getime(),os.path.join(copy_dict[i],'.updatime'))
    print('copy dir finished!')
    print('{} --> {} '.format(source_path, target_path))
    print()

