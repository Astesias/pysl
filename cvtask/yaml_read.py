import yaml
import os

file = open('./yml.yml', 'r')
file_data = file.read()
file.close()

data = yaml.load(file_data,Loader=yaml.FullLoader)





















# def get_yaml_data(yaml_file):
#     # 打开yaml文件
#     print("***获取yaml文件数据***")
#     file = open(yaml_file, 'r', encoding="utf-8")
#     file_data = file.read()
#     file.close()
    
#     print(file_data)
#     print("类型：", type(file_data))

#     # 将字符串转化为字典或列表
#     print("***转化yaml数据为字典或列表***")
#     data = yaml.load(file_data)
#     print(data)
#     print("类型：", type(data))
#     return data


# get_yaml_data('./yml.yml')