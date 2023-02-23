def intToY(num,Y):
    res = ""
    while (num!=0):
        # temp=
        # temp=
        res = str(NumToABC(num%Y))+res
        num = num//Y #取商
    # res = int(res)
    res.upper()
    return res

def ABCToNum(char):
    if char in "0123456789":
        return int(char)
    if char in "Aa" :
        return 10
    if char in "Bb":
        return 11
    if char in "Cc" :
        return 12
    if char in "Dd":
        return 13
    if char in "Ee" :
        return 14
    if char in "Ff":
        return 15
#  辅助功能函数
def NumToABC(intN):
    if intN in [0,1,2,3,4,5,6,7,8,9]:
        return intN
    if intN ==10 :
        return 'A'
    if intN ==11 :
        return 'B'
    if intN ==12 :
        return 'C'
    if intN ==13 :
        return 'D'
    if intN ==14 :
        return 'E'
    if intN ==15 :
        return 'F'