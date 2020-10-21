from jSona import save, load
import traceback

class Family :
    def __init__(self) :
        self.family = list()
        self.count  = 0
    
    def __call__(self) :
        print(self.family)

    def size(self) :
        return len(self.family)

    def add(self, kitty) : 
        if kitty : 
            self.family.append(kitty)
            self.count += 1
            return True
        else :
            return False

    def save(self, cpath) :
        save(cpath, self.family)

class Kitty :
    def __init__(self, **kwargs) :
        self.value = kwargs

    def __call__(self) :
        return self.value