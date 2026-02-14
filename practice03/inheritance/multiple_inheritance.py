# Example: multiple inheritance + MRO

class A:
    def info(self):
        print("Class A")

class B:
    def info(self):
        print("Class B")

class C(A, B):
    pass

x = C()
x.info()
print(C.mro())
