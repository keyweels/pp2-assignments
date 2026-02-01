n = int(input())
maxi = -9999
mini = -9999
while n > 0:
    last_digit = n % 10
    if last_digit > maxi:
        maxi = last_digit
    elif last_digit < mini:
        mini = last_digit
    n /= 10
print(maxi, mini)