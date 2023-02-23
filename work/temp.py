import os
import json
import shutil

download_path='./download'
output_path='./output'
for dp in os.listdir(download_path):
    # print(dp)
    dp2=os.path.join(download_path,dp)
    dp3=os.listdir(dp2)[0]
    dp4=os.path.join(dp2,dp3)
    jsp=os.path.join(dp4,'entry.json')
    js=json.load(open(jsp))
    title=js['title']
    for _ in '<>\":?*/\\|':
        title=title.replace(_,'')
    
    dp5=os.path.join(dp4,'16')
    audio=os.path.join(dp5,'audio.m4s')
    
    rename_file=os.path.join(dp5,title+'.mp3')
    output_file=os.path.join(output_path,title+'.mp3')
    
    os.renames(audio,rename_file)
    shutil.copy(rename_file,output_file)