# Practical lambda with filter(): select elements by condition

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]

evens = list(filter(lambda n: n % 2 == 0, numbers))
print(evens)

words = ["python", "lambda", "filter", "sorted", "class"]
long_words = list(filter(lambda w: len(w) > 5, words))
print(long_words)
