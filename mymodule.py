# mymodule

x = 0

def add1(n):
    return n+1

def add2(n):
    return n+2

def add3(n):
    return add1(n)+add2(n)

class MyClass:
    def __init__(self):
        self.i = 0

    def incr(self):
        self.i = self.i + 1
        print(str(self.i))

    def incr2(self):
        global x
        x = x + 1
        print(str(x))

print("hihihi")
