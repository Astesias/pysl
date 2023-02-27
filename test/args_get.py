import argparse

# parser = argparse.ArgumentParser(description='argments get')
# parser.add_argument('-epochs', type=int, default=30)
# parser.add_argument('-batch', type=int, default=4)

# args = parser.parse_args()

# epochs = args.epochs
# batch = args.batch

# print('show {}  {}'.format(epochs, batch))


#       name    argname  type  default  help     
dicts={
        'num_i':('-n',int,),
        'num_f':('-f',float),
        'str':('-s',str),

        }


def add_argments(dicts,help='argments get'):
    parser = argparse.ArgumentParser(description=help)
    for k,v in dicts.items():
        argname,types,*_=v
        if _:
            default=_[0]
            if len(_)>=2:
                help_=_[-1]
            else:
                help_='None'
        else:
            default=None
            help_='None'

        parser.add_argument(argname, type=types, default=default,help=help_)
    return parser.parse_args()

arg=add_argments(dicts)
print(arg.f)











