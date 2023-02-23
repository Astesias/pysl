from pysl import for_list
class aniter():
    def __init__(self,item):
        if '__iter__' not in dir(item):
            raise TypeError
        self.item=item
        self.n=-1
    def __next__(self):
        self.n+=1
        if self.n>len(self.item)-1:
            self.n=0
        return self.item[self.n]
    def __iter__(self):
        return iter(self.item)

def yielder(item):
    item=for_list(item)
    for i in item:
        yield i