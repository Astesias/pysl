import time
import random
import numpy as np
from pysl import random_name,mmap

class Deck():
    default_deck=( (['A','K','Q','J','H']+[str(i) for i in range(2,10)])*4+['w','W'] )
    def __init__(self,deck=default_deck,sp_num=3):
        deck=self.deck_sort(deck)
        self.PLAYER=self.TOTAL=self.SP=False
        if len(deck)!=Deck.default_deck and len(deck)!=sp_num:
            self.PLAYER=True
        elif len(deck)==Deck.default_deck:
            self.TOTAL=True
        else:
            self.SP=True
            
        deck=np.array(deck)
        self._deck=deck
        
    def sample(self,n=None):
        if not n:
            n=len(self._deck)
        if n>len(self._deck):
            raise Exception('Not enough')     
        dc=self._deck.copy()
        samples=np.random.choice(len(self._deck),n,replace=False)
        self._deck=np.delete(self._deck,samples)
        return Deck(dc[samples])
    
    def _left(self):
        return len(self._deck)
    
    def _show(self):
        return self._deck
    
    def deck_sort(*deck):
        # print(deck)
        l=['W','w','2','A','K','Q','J','H']+[str(i) for i in range(9,2,-1)] 
        try:
            return sorted(deck[1],key=lambda x:l.index(x))
        except:
            return sorted(deck[0],key=lambda x:l.index(x))
    
    
class Player():
    playerlist=[]
    host_name=''
    def __init__(self,name=None):
        self._=1
        self.set_name(name)
        
    def set_name(self,name,n=4):
        if name==None:
            name='player_'+random_name(n)
        self.name=name
        if name not in  Player.playerlist:
            Player.playerlist.append(name)
        else:
            raise Exception('Set name failed,try again')
        print(f'Your name is {name}')
          
    def set_host(self):
        Player.host_name=self.name
        
    def ishost(self):
        return self.name==Player.host_name
    
    def set_deck(self,deck):
        assert isinstance(deck,Deck)
        self.deck=deck
        
    def show_deck(self):
        _=0
        print(self.name,end=': ')
        for n,i in enumerate(self.deck._deck):
            if i=='W':
                print('W',end='')
            elif i=='w':
                print('w',end='')
            elif _==i:
                print(''+i,end='')
            else:
                print((' ' if n!=0 else '')+i,end='')
            _=i
        print()
    
    def put(self,string):
        ldeck=list(self.deck._deck)

        for s in string:
            try:
                if s.lower()!='w':
                    s=s.upper()
            except:
                pass
            ldeck.remove(s)

        self.deck._deck=Deck.deck_sort(np.array(ldeck))
        
    @classmethod
    def gethost(cls):
        return cls.host_name
        
class GameField():
    def __init__(self,p1,p2,p3):
        assert isinstance(p1,Player)
        assert isinstance(p2,Player)
        assert isinstance(p3,Player)
        self.p1=p1
        self.p2=p2
        self.p3=p3
        self.plist=plist=[p1,p2,p3]
        self._=1
        
        p_sp=self.robhost()
        p_sp.set_host()

        deck=Deck()
        for p in plist:
            p.set_deck(deck.sample(17))
            p.show_deck()
        sp=deck.sample(3)
        print('hostboard: ',sp._deck)
        p_sp.deck=Deck(np.concatenate((p_sp.deck._deck,sp._deck)))
        
        p_sp.show_deck()
        
        self.nowturn=plist.index(p_sp)
        
        
    def robhost(self):
        h=random.choice(self.plist)
        self.p_sp=h
        print('Host:',h.name)
        print()
        return h
    
    def runtine(self):
        while not self.iswin():
            print()
            for p in self.plist:
                p.show_deck()
            print()
                
            eventid=input(f'Turn to {self.plist[self.nowturn].name}: ').replace(' ','')
           
            GameField.event(self.plist[self.nowturn],eventid)
            self.nowturn+=1
            self.nowturn%=3

        print(self.iswin().name,' winning')
            
    def event(player,eventid):
        if eventid=='0':
            pass
        elif type(eventid)==type(''):
            # print(len(np.intersect1d(list(eventid),player.deck._deck)),len(list(eventid)))
            # assert len(np.intersect1d(list(eventid),player.deck._deck))==len(list(eventid))
            player.put(eventid)
        
    def iswin(self):
        for n,p in enumerate(self.plist):
            if not len(p.deck._deck):
                return p
        else:
            return False
    
if __name__ == '__main__':
    
    # deck=Deck()
    # deck._left()
    # print(deck.sample(54)._left())
    # deck._left()
    
    p1=Player('p1')
    p2=Player('p2')
    p3=Player('p3')
    # print(p1.gethost())
    
    g1=GameField(p1,p2,p3)

    # TODO putchecker putsorter
    
    pass