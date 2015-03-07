from gmpy2 import mpz, gcd

def PollardRho(n, a=1):
    f = lambda x: (x**2 + a) % n
    tortoise = f(2)
    hare = f(f(2))
    factor = 1
    while gcd(factor,n) == 1:
        tortoise = f(tortoise)
        hare = f(f(hare))
        factor = gcd(abs(tortoise-hare), n)
    if factor == n:
        return None
    return gcd(factor,n)

#Now, bring in the tempest prime testing

def factorize(n, printPartial=False):
    n = mpz(n)
    factorization = []
    if isPrime2(n): return [n]
    for prime in xrange(2, 1000):
        if n % prime == 0:
            while n % prime == 0:
                factorization.append(prime)
                n /= prime
    a = 1
    while n != 1 and (not isPrime2(n)):
        factor = PollardRho(n, a)
        if factor:
            while n % factor == 0:
                factorization += factorize(factor)
                n /= factor
                if printPartial: print factor
        else:
            a += 1
            #print a, n
    if n != 1: factorization.append(n)
    return factorization

'''Down here is copied from tempest prime testing, for now.'''

#is_prime(number) -> {True, False}
#This tests whether a number is probably prime.
        
def MillerRabin(number, base):
    oddpart = number-1
    evencount = 0
    while oddpart % 2 == 0:
        evencount += 1
        oddpart >>= 1 #Now oddpart*2^evencount == number

    power = pow(base, oddpart, number)
    if power == number - 1 or power == 1: return True
    for i in xrange(evencount-1):
        power = (power**2) % number
        if power == number - 1: return True
        if power == 1: return False #Found a quadratic congruence!
    return False #Will not reach 1!

import random
from random import *

def isPrime2(number):
    # Ignores initial trial division.
    if number < 2: return False
    if number == 2 or number == 3: return True
    if number < 1373652: return MillerRabin(number, 2) and MillerRabin(number, 3)
    if number < 4759123141: return MillerRabin(number, 2) and MillerRabin(number, 7) and MillerRabin(number, 61)
    supertest = MillerRabin(number, 2) and MillerRabin(number, 3) and MillerRabin(number, 5) and MillerRabin(number, 7) and MillerRabin(number, 11) and MillerRabin(number, 13) and MillerRabin(number, 17)
    if number < 341550071728321: return supertest
    for i in xrange(5):
        if not MillerRabin(number, randint(1000000, number-1000000)): return False
    return True #Probably prime.

def isPrime(number):
    number = mpz(number)
    # Trial division through 1000, followed by isPrime2.
    L = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,
         71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139,
         149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
         227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293,
         307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383,
         389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
         467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569,
         571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647,
         653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743,
         751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839,
         853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941,
         947, 953, 967, 971, 977, 983, 991, 997]
    for p in L:
        if number % p == 0:
            return number == p
    return isPrime2(number)

try:
    import numpy as np
except:
    pass

def sieve(n):
    # http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = np.ones(n/3 + (n%6==2), dtype=np.bool)
    sieve[0] = False
    for i in xrange(int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[      ((k*k)/3)      ::2*k] = False
            sieve[(k*k+4*k-2*k*(i&1))/3::2*k] = False
    return np.r_[2,3,((3*np.nonzero(sieve)[0]+1)|1)]
                





