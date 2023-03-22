import os
import json

def setcfg():
    try:
        os.mkdir('./scoretxt')
        print('创建乐谱目录')
    except:
        # print('乐谱目录存在')
        pass
    
    ts=os.listdir('./scoretxt')
    cfg={}
    for _ in ts:
        with open(os.path.join('./scoretxt',_)) as fp:
            d=fp.read()
            tp=1 if (d.count('W') >= d.count('+2')) else 0
        cfg[_]={'bpm':None,'type':tp}
    if not cfg:
        print('未检测到乐谱')
    
    if not os.path.exists('cfg.json'):
        with open('cfg.json','w') as fp:
            json.dump(cfg,fp,ensure_ascii=False,indent=2)
    else:
        with open('cfg.json') as fp:
            newcfg=json.load(fp)
        cfg.update(newcfg)
        
        with open('cfg.json','w') as fp:
            json.dump(cfg,fp,ensure_ascii=False,indent=2)

    return cfg

    
if __name__ == '__main__':
    print(setcfg())