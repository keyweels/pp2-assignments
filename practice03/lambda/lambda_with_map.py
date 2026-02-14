# Practical lambda with map(): transform each element

numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda n: n * n, numbers))
print(squared)

names = ["emil", "tobias", "linus"]
uppercased = list(map(lambda s: s.upper(), names))
print(uppercased)
