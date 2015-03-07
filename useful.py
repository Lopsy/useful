def index():
    print "factorize(n), isPrime(n), nextPrime(n), sieve(n), gcd(a,b)\n"+\
           "binom(n,k), fib(n)\n"+\
           "wchoice(array of [obj,weight])\n"+\
           "subsets(L)\n"+\
           "@memoize\n"+\
           "dictionary(common=True)"+\
           "visca(r'regex')"
           
help=index

from primes import isPrime, sieve#, factorize
from ellipticCurves import factorize
from memoize import memoize
from gmpy2 import mpz, gcd
from random import random

def nextPrime(n):
    while not isPrime(n): n += 1
    return n

'''def gcd(a,b):
    while b != 0:
        a, b = b, a%b
    return a''' # gcd from the gmpy2 module

def binom(n,k):
    t = 1
    i = n-k+1
    while i <= n:
        t *= i
        i += 1
    i = 1
    while i <= k:
        t /= i
        i += 1
    return t

@memoize
def fib(n):
    if n<3: return mpz([0,1,1][n])
    if n%2==0: return fib(n/2+1)**2-fib(n/2-1)**2
    return fib(n/2)**2+fib(n/2+1)**2

def wchoice(ary):
    ''' ary is like [ (apple,1), (banana,3), (orange,2.5) ] '''
    total = sum(map(lambda x:x[1],ary))
    windex = random()*total
    for a in ary:
        if windex < a[1]:
            return a[0]
        windex -= a[1]
    crash

def subsets(L):
    if len(L) == 0:
        yield []
        raise StopIteration
    for subset in subsets(L[1:]):
        yield subset
        yield subset+[L[0]]

def dictionary(common=False):
    '''Returns a list of English words mostly sorted by frequency.
    Generally lowercase, except for words like "I".
    Thanks to http://wordlist.sourceforge.net/12dicts-readme-r5.html
    and the Scrabble dictionary.

    dictionary(common=True) only uses the more everyday words.'''
    import re
    word = re.compile(r"(^| |[^a-zA-Z])([a-zA-Z]+)")
    with open('dictionaryfreq.txt','r') as f:
        W = f.read()
    if not common:
        with open('dictionary.txt','r') as f:
            W2 = f.read()
        W = W+" "+W2.lower()
    M = re.findall(word,W)
    L, S = list(), set()
    for (char1,word) in M:
        if word not in S:
            S.add(word)
            L.append(word)
    return L

def visca(string):
    words = []
    from re import search, compile
    R = compile(string)
    for word in dictionary():
        if search(R,word):
            words.append(word)
    return words
