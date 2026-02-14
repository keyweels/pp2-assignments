# Examples: class variable vs instance variables (simple)

class Person:
    species = "Human"

    def __init__(self, name, age):
        self.name = name
        self.age = age

p1 = Person("John", 36)
p2 = Person("Sally", 25)

print(Person.species)
print(p1.name, p1.age, p1.species)
print(p2.name, p2.age, p2.species)

Person.species = "Homo sapiens"
print(p1.species)
print(p2.species)
