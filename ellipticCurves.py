""" Treats elliptic curves of the form

y^2 = x^3 + ax + b

Here any variable called "curve" is going to be a tuple (a,b).

A point on a curve is a tuple (x,y),
    OR the number 0 representing the point at infinity.

Works with Mod from the modulo module."""

#from Polynomial import Poly, var
from gmpy2 import gcd

x,y = var(24),var(25)


def myNaiveFactorize(n):
    from random import randint
    from modulo import Mod
    from useful import sieve
    def times(curve, p, k):
        """naive method"""
        point = p
        for i in xrange(k-1):
            try:
                point = add(curve, point, p)
            except:
                if point == p:
                    return "WOO",2*p[1]
                else:
                    return "WOO",point[0]-p[0]
        return point
    def randomCurveAndPoint(n):
        def m(k): return Mod(k,n)
        a,x,y = m(randint(1,n)),m(randint(1,n)),m(randint(1,n))
        b = y**2 - x**3 - a*x
        return (a,b),(x,y)
    while True:
        curve, P = randomCurveAndPoint(n)
        i = 2
        limit = 300
        for i in xrange(2,limit):
            P = times(curve, P, i)
            if type(P)==tuple and P[0]=="WOO":
                return gcd(P[1].n,n)
            if P == 0: break

from primes import isPrime, sieve
from gmpy2 import iroot, mpz, gcd
from math import log
from random import randint

def tryToFindFactor(n, B2=2000):
    B1, B2 = 1000, B2
    s = randint(6,n-1)
    u = s**2 - 5
    v = 4*s
    An = ((v-u)**3 * (3*u+v)) % n
    Ad = (4*u**3*v) % n
    P = (mpz(u**3)%n,mpz(v**3)%n)
    def add((x1,z1),(x2,z2),(x0,z0)):
        w, v = (x1-z1)*(x2+z2) % n, (x1+z1)*(x2-z2) % n
        return (((w+v)**2 * z0) % n,
                ((w-v)**2 * x0) % n)
    def double((x,z)):
        w, v = (x+z)**2 % n, (x-z)**2 % n
        t = w - v
        return (((w*v*4*Ad) % n,
                ((4*Ad*v+t*An)*t) % n))
    def times((x,z),k):
        cache = {1: (x,z)}
        def do(m):
            """Updates the cache with (x,z) multiplied m times."""
            if m in cache: return cache[m]
            if m % 2 == 0:
                half = do(m/2)
                answer = double(half)
            else:
                lessThanHalf = do(m/2)
                moreThanHalf = do(m/2+1)
                answer = add(lessThanHalf,moreThanHalf,P)
            cache[m] = answer
            return answer
        return do(k)
    for p in sieve(B1):
        a = int(log(B1,p))
        P = times(P, p**a)
        g = gcd(P[1],n)
        if 1 < g < n: return g # Woo!
    for p in sieve(B2):
        if p >= B1:
            P = times(P, p)
            g = gcd(P[1],n)
            if 1 < g < n: return g # Woo!
        
def factorOf(n):
    i = 0
    while True:
        i += 1
        F = tryToFindFactor(n, 2000+200*i)
        if F: return F, i
        
def factorize(n):
    prefactors, n = smallFactors(n)
    if n == 1: return prefactors
    return sorted(prefactors+bigFactorize(n))

def bigFactorize(n):
    factors = []
    power = isPower(n)
    if power: # then power = (i, root)
        return bigFactorize(power[1])*power[0]
    while not isPrime(n):
        f = factorOf(n)[0]
        factors.extend(bigFactorize(f))
        n /= f
    return factors+[n]
def isPower(n):
    i = 2
    while True:
        ithroot = iroot(n, i)
        if ithroot[1]: # if perfect ith root
            return (i, ithroot[0]) # return i, root
        if ithroot[0] < 1000: return False
        i += 1
def smallFactors(n):
    factors = []
    for p in sieve(1000):
        while n%p==0:
            factors.append(p)
            n /= p
    return factors, n


def poly(curve):
    (a,b) = curve
    return x**3 + a*x + b - y**2

def add(curve, p, q):
    (a,b) = curve
    if p == q: # This case works! I think. I've checked it.
        if p == 0: return 0
        # dF/dx = 3x^2+a
        # dF/dy = -2y
        slope = (3*p[0]**2 + a)/(2*p[1])
    else: # This case works!! I've checked it. Except maybe on specific cases.
        if p == 0: return q
        if q == 0: return p
        if p[0]==q[0]: return 0
        slope = (p[1]-q[1])/(p[0]-q[0])
    # line is y = slope*(x-p[0])+p[1]
    # x**3 + a*x + b - (slope*(x-p[0])+p[1])**2
    # leading coefficient 1
    # next coefficient -slope^2
    # so sum of roots is slope^2
    x = slope**2 - p[0] - q[0]
    y = slope*(x-p[0])+p[1]
    return (x,-y)

def times(curve, p, n):
    """super naive"""
    point = 0
    for i in xrange(n):
        point = add(curve, point, p)
    return point
