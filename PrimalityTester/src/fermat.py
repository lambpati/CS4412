import math
import random


def prime_test(N, k):
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N, k), miller_rabin(N, k)


def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.
    if y == 0:
        return 1
    z = mod_exp(x, math.floor(y / 2), N)
    if (y % 2) == 0:
        return math.pow(z, 2) % N
    else:
        return x * (math.pow(z, 2) % N)


def fprobability(k):
    # You will need to implement this function and change the return value.
    pr = 1 / (math.pow(2, k))
    return pr


def mprobability(k):
    # You will need to implement this function and change the return value.   
    pr = 1 / (math.pow(4,k))
    return pr


def fermat(N, k):
    a = []
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    assert (k < N), "k is greater than N!"
    for i in range(k):
        a.append = random.randint(1, N - 1)
    if mod_exp(a, N - 1) == 1 % N:
        return 'prime'
    else:
        return 'composite'


def miller_rabin(N, k):
    y = N - 1
    a = []
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.
    assert (k < N), "k is greater than N!"
    for i in range(k):
        a.append = random.randint(1, N - 1)
    while y % 2 == 0:
        y //= 2
    if mod_exp(a, y, N) != 1 or mod_exp(a, y, N) != N-1:
        return 'composite'
    else:
        return 'prime'