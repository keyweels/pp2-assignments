#1
print("Hello")
print('Hello')

#2
print("It's alright")
print("He is called 'Johnny'")
print('He is called "Johnny"')

#3
a = "Hello"
print(a)

#4
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
print(a)

#5
a = '''Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua.'''
print(a)

#6
a = "Hello, World!"
print(a[1])

#7
for x in "banana":
  print(x)

#8
a = "Hello, World!"
print(len(a))

#9
txt = "The best things in life are free!"
print("free" in txt)

#10
txt = "The best things in life are free!"
if "free" in txt:
  print("Yes, 'free' is present.")

#11
txt = "The best things in life are free!"
print("expensive" not in txt)

#12
txt = "The best things in life are free!"
if "expensive" not in txt:
  print("No, 'expensive' is NOT present.")

#13
b = "Hello, World!"
print(b[2:5])

#14
b = "Hello, World!"
print(b[:5])

#15
a = "Hello, World!"
print(a.upper())

#16
a = "Hello, World!"
print(a.lower())

#17
a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

#18
a = "Hello"
b = "World"
c = a + b
print(c)

#19
a = "Hello"
b = "World"
c = a + " " + b
print(c)

#20
age = 36
txt = f"My name is John, I am {age}"
print(txt)

#21
price = 59
txt = f"The price is {price} dollars"
print(txt)

#22
price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)

#23
txt = f"The price is {20 * 59} dollars"
print(txt)

#24
txt = "We are the so-called \"Vikings\" from the north."