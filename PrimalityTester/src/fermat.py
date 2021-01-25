import math
import random


def prime_test(N, k):
    # This is main function, that is connected to the Test button. You don't need to touch it.
    return fermat(N, k), miller_rabin(N, k)


def mod_exp(x, y, N):
    # Based on Pseudocode 1.4, page 19 states runtime is O(log^2(n))
    if y == 0:
        return 1
    z = mod_exp(x, y // 2, N)
    if (y % 2) == 0:
        return z ** 2 % N
    else:
        return x * z ** 2 % N


def fprobability(k):
    # According to the book, Pseudocode 1.8 has a probability function of 1- 1/2^k, where k is the number of the
    # times iterated
    pr = 1 - 1 / (math.pow(2, k))  # O(n)
    return pr


def mprobability(k):
    # According to the book, in worst case scenerio (k=1), then 3/4 times the Miller-Rabin Function
    # will determine a composite, therefore the equation would be 1 - 1/4^k as the more iterations
    # occur, the more certain the result is a prime becomes.
    pr = 1 - 1 / (math.pow(4, k))  # O(n)
    return pr


def fermat(N, k):
    # Fermat's test works via a randomly generated int, "a" between 2 and N
    # and checks to make sure k does not exceed N and then using mod_exp to check if a^(N-1)(mod N) = 1,
    # and returns 'prime' if its a prime number
    # Fermat's theorem is O(n^4)
    assert (k < N), "k is greater than N!"
    for i in range(k):  # O(n)
        a = random.randint(2, N)  # O(1)
        if mod_exp(a, N - 1, N) == 1 % N:  # O(log^2(n)) + O(log(n))
            return 'prime'  # O(1)
    return 'composite'  # O(1)


def miller_rabin(N, k):
    # Fermat's test works via a randomly generated int, "a" between 2 and N
    # and checks to make sure k does not exceed N. Then, to save time, it reduces the exponential term, 'y' by 2 until
    # y (mod 2) != 0. Using mod_exp, it checks if a^(N-1)(mod N) = 1 and a^(2^(t)*u) (mod N) = N - 1 over t
    # Time complexity is O(n^2)
    t = 0
    y = N - 1
    while y % 2 == 0:  # O(n)
        y >>= 1
        t += 1
    assert (2 ** t * y == N - 1)
    assert (k < N), "k is greater than N!"
    for i in range(k):  # O(n)
        a = (random.randint(2, N))  # O(1)
        if mod_exp(a, y, N) == 1:  # O(log^2(n)) + O(n)
            return 'prime'  # O(1)
        for j in range(t):  # O(n)
            if mod_exp(a, 2 ** j * y, N) == N - 1:  # O(log^2(n))* O(log^2(n)) + O(1)
                return 'prime'  # O(1)
    return 'composite'  # O(1)
