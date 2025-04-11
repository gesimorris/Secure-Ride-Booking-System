import random
import math

# Generate a random prime number
def generatePrimeNumber():
    while True:
        num = random.randint(10,38)
        for i in range (2, int(math.sqrt(num))+1):
            if num % i == 0:
                break
        else:
            return num
        
# Calculate Modular Inverse
def modInverse(a, m):
    t, new_t = 0, 1
    r, new_r = m, a
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return None
    return t + m if t < 0 else t
        
# Generate Keys
def generateKeys():
    p = generatePrimeNumber()
    q = generatePrimeNumber()
    n = p*q
    phi = (p-1)*(q-1)

    # Find e part of the public key
    e = random.randint(2, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = modInverse(e, phi)
    if d:
        public_key = [e, n]
        private_key = [d, n]
        return public_key, private_key

# Encrypt
def encrypt(message,key):
    e, n = key
    return [pow(ord(char), e, n) for char in message]

# Decrypt
def decrypt(cipher,key):
    d, n = key
    return ''.join([chr(pow(char, d, n)) for char in cipher])


