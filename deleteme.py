from random import choice
from string import ascii_uppercase


line2s = []
apt_letters = [c for c in ascii_uppercase]
apt_numbers = [str(n) for n in range(101, 999)]

while len(line2s) < 48:

    if choice((True, False)):

        if choice((True, False)):
            apt = choice(apt_numbers)
        else:
            apt = choice(apt_letters)

        line2s.append(' '.join(('Apt.', apt)))

    else:

        line2s.append(None)

print(line2s)