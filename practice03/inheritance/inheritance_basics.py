# W3Schools style examples: inheritance basics (Student inherits from Person)

class Person:
    def __init__(self, fname, lname):
        self.firstname = fname
        self.lastname = lname

    def printname(self):
        print(self.firstname, self.lastname)

x = Person("John", "Doe")
x.printname()


class Student(Person):
    pass

x2 = Student("Mike", "Olsen")
x2.printname()
