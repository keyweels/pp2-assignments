import random

print(random.random())
print(random.randint(1, 10))
print(random.choice(["apple", "banana", "cherry"]))

nums = [1, 2, 3, 4, 5]
random.shuffle(nums)
print(nums)
