import sys
import os


def main(system_ord):
    with open(system_ord,encoding='utf-8') as fp:
        data=fp.read()
        print(data)
    
if __name__ == '__main__':
    system_ord=sys.argv[1]
    for i in sys.argv:
        print(i)
    main(system_ord)
    print('\nenter to quit')
    n=input()