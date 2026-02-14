# Practical lambda with sorted(): custom sorting key

thislist = ["orange", "mango", "kiwi", "pineapple", "banana"]
thislist_sorted = sorted(thislist, key=lambda x: len(x))
print(thislist_sorted)

students = [
    {"name": "Emil", "age": 20},
    {"name": "Tobias", "age": 19},
    {"name": "Linus", "age": 21},
]
students_sorted = sorted(students, key=lambda s: s["age"])
print(students_sorted)
