from random import random, choice
from math import floor


addresses = []
numbers = []
st_numbers = [n for n in range(1, 25)]
st_suffixes = ['St.', 'Ave.']

while len(numbers) < 48:

    rand_int = int(floor(random() * 1000))

    if rand_int > 0 and rand_int not in numbers:
        numbers.append(str(rand_int))


while numbers:

    number = numbers.pop()
    st_number = str(choice(st_numbers))

    if st_number in ('11', '12', '13') or st_number[-1] not in ('1', '2', '3'):
        st_number += 'th'
    else:
        if st_number[-1] == '1':
            st_number += 'st'
        elif st_number[-1] == '2':
            st_number += 'nd'
        else:
            st_number += 'rd'

    suffix = choice(st_suffixes)

    addresses.append(' '.join((number, st_number, suffix)))

print(addresses)