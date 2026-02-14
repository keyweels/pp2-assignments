# W3Schools style examples: *args and **kwargs

def my_function(*args):
    print(args[0])

my_function("Hello", "World")


def my_function2(*kids):
    print("The youngest child is " + kids[2])

my_function2("Emil", "Tobias", "Linus")


def my_function3(**kid):
    print("His last name is " + kid["lname"])

my_function3(fname="Tobias", lname="Refsnes")
