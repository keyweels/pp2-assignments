def mygenerator():
    yield 1
    yield 2
    yield 3

for x in mygenerator():
    print(x)
