import re

class sympy():
    def __init__(self,func_str):
        
        var = re.compile(r'[a-zA-Z_]+[a-zA-Z0-9]*')
        state = re.compile(r'[\-+]?[a-zA-Z0-9][^(+|\-)]+')
        var_list=var.findall(func_str)
        state_list=state.findall(func_str)
        print(var_list,state_list,sep='\n')
        
        s=''
        for va in var_list:
            s+=va+','
        s.rstrip(',')
            
        exec('self.func=lambda {}:{}'.format(s,func_str))
        print(self.func(1,1,0,0))
        self.vars=var_list
        self
        
        
        
func_str='2*x**3+5*y-z/3*k'
func=sympy(func_str)

#[+\-]?([0-9]*[+\-\*])?[a-zA-Z_]+[a-zA-Z0-9]*([(\*\*)/]+[0-9]+)?