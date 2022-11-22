class dicter:
    # x=7
    def __init__(self):
        self.a= {}

    def creat(self,key,name):
        self.a[key]=name

    def prnt(self):
        print(self.a)
        # dicter.p(4)
    @staticmethod
    def p(x):
        print(x)



dict=dicter()
dict2=dicter()

dict.creat("5",7)
dict.creat("6",9)
dict.creat("18",9)

dict.prnt()
dict2.prnt()

# dict.p(4)

