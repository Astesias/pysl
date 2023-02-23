
def main(otherdir=None):
######################  create empty files in teamname(1000000)/NUDT 
    names=[]
    for i in range(1,201):
        names.append('{:0>4}.txt'.format(i))
    
    if otherdir:
        for name in names:
            with open(otherdir+name,'w') as f:
                f.write('Team: 1000000\n')
    
    for name in names:
        with open('NUDT/NUDT/'+name,'w') as f:
            f.write('Team: 1000000\n')
            
    print('空结果生成')
if __name__ == '__main__':
    main()
            