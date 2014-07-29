from random import random
from math import floor

numbers = []

while len(numbers) < 52:
    rand_num = str(int(floor(random() * 10000))).zfill(4)
    if rand_num not in numbers:
        numbers.append(rand_num)


print(numbers)