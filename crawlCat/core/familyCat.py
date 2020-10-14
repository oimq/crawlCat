import json
import traceback

class Cats :
    def __init__(self) :
        self.family = list()
    
    def __call__(self) :
        print(self.family)

    def add(self, kitty) : 
        if kitty : self.family.append(kitty())
        return kitty

    def error(self, e, msg="") :
        print("ERROR {} : {}".format(msg, e))
        traceback.print_exc()

    def saveJson(self, cpath, table) :
        try :
            with open(cpath, 'w') as openfile :
                json.dump(table, openfile)
            print("\nSave data success. {}\n".format(cpath))
        except Exception as e :
            self.error(e, "SAVE JSON")

    def save(self, cpath) :
        self.saveJson(cpath, self.family)

class Kitty :
    def __init__(self, **kwargs) :
        self.value = kwargs

    def __call__(self) :
        return self.value