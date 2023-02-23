

def make_json(name):
    import re
    with open('temp.json') as fp:
        data=fp.read()
    # data='\n'.join(data)
    print(data)
    
    keys=re.findall('.+?(?=:): ',data)
    values=re.findall('(?<= ).+',data)
    
    with open(name+'h.json','w') as fp:
        fp.write('{\n')
        for i,j in zip(keys,values):
            i=i.strip(': ')
            fp.write(f'\"{i}\": \"{j}\",\n')
        
        fp.write(r'"py": "ysl"')
        fp.write('\n}')

if __name__ == '__main__':
    make_json('0_')