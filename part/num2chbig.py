import random

def get_ch(a):
    num_dict = {'0': '零', '1': '壹', '2': '贰', '3': '叁', '4': '肆', '5': '伍', '6': '陆', '7': '柒', '8': '捌', '9': '玖'}
    units = ['', '拾', '佰', '仟', '万', '拾', '佰', '仟', '亿']
    rep = [('零零', '零圆', '零拾', '零佰', '零仟', '零万', '零亿', '亿万',), ('零', '圆', '零', '零', '零', '万', '亿', '亿',)]
    string = '圆'
    num = 0
    for i in str(abs(a))[-1::-1]:
        string = num_dict[i] + units[num] + string
        num += 1
        for z, v in zip(rep[0], rep[1]):
            string = string.replace(z, v)
        if num == 9:
            num = 1
    if a == 0:
        string = '零圆'
    elif a < 0:
        string = '负' + string
    return string

def num2strcn(a):
    num = {0:u'零',1:u'壹',2:u'贰',3:u'叁',4:u'肆',5:u'伍',6:u'陆',7:u'柒',8:u'捌',9:u'玖'}
    er = {0:'',1:u'拾',2:u'佰',3:u'仟',4:'万',-1:u'圆'}
    string=''
    
    if a<0:
        string+=u'负'
        a=-a
    
    a1=str(a//10000)
    a2='{:0>4}'.format(a-10000*int(a1)) if a>=10000 else str(a-10000*int(a1))

    l1=len(a1)
    l2=len(a2)
    
    for n,i in enumerate(a1):
        i=int(i)
        if i:
            string+=(num[i]+er[l1-n-1])
        else:
            try:
                inext=int(a1[n+1])
            except:
                continue
            if inext:
                string+=num[0]
            else:
                continue
    if int(a1):
        string+=er[4]

        
    for n,i in enumerate(a2):
        i=int(i)
        if i:
            string+=(num[i]+er[l2-n-1])
        else:
            try:
                inext=int(a2[n+1])
            except:
                continue
            if inext:
                string+=num[0]
            else:
                continue
    if a:
        string+=er[-1]
    else:
        string+=(num[0]+er[-1])
    return string


# la=random.randint(1,7)
# a=random.randint( 10**la , 10**(la+1)-1 )

# for i in range(0,10000000):
#     if get_ch(i)!=num2strcn(i):
#         print(get_ch(i),num2strcn(i))


print(get_ch(100212))