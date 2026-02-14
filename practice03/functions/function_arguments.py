# W3Schools style examples: positional, default, *args, **kwargs, list as argument

def my_function(fname, lname):
    print(fname + " " + lname)

my_function("Emil", "Refsnes")


def my_function_children(*kids):
    print("The youngest child is " + kids[2])

my_function_children("Emil", "Tobias", "Linus")


def my_function_country(country="Norway"):
    print("I am from " + country)

my_function_country("Sweden")
my_function_country("India")
my_function_country()
my_function_country("Brazil")


def my_function_food(food):
    for x in food:
        print(x)

fruits = ["apple", "banana", "cherry"]
my_function_food(fruits)


def my_function_kwargs(**kid):
    print("His last name is " + kid["lname"])

my_function_kwargs(fname="Tobias", lname="Refsnes")
