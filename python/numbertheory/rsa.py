from prime import random_n_bit_long_prime
from euclid_alg import euclid_gcd, modular_division
from util import convert_to_int, convert_to_str, binary_expansion

'''
Steps to generate RSA keys:

- Select two very large prime numbers p and q.
- Compute n = pq and φ(n) = (p – 1)(q – 1).
- Choose an encryption key e relatively prime to φ(n).
- Calculate the decryption key d such that ed = 1 (mod φ(n)).
- Publish e and n, and keep d, p, and q secret.

Common practice is to generate exponent e first, normally the fixed value 65537, and then generate
the primes p and q as many times as it takes to find values such that gcd(a, φ(n)) = 1

See https://www.johndcook.com/blog/2018/12/12/rsa-exponent/
'''


class RSA:

    e = 65537

    def __init__(self, n):
        p, q = RSA.generate_private_key(n)
        self.n = RSA.generate_public_key(p, q)
        self.num_bits_of_n = len(binary_expansion(self.n))
        self.d = RSA.calculate_decryption_exponent(p, q)
        # print(f"p {p}")
        # print(f"q {q}")
        # print(f"n {self.n}")
        # print(f"d {self.d}")

    @staticmethod
    def generate_private_key(n):
        '''
        Generate a private key n-bit long
        A private key is a pair of large prime numbers (p, q)
        '''
        p, q = (random_n_bit_long_prime(n), random_n_bit_long_prime(n))
        phi = (p - 1)*(q-1)
        if euclid_gcd(RSA.e, phi) > 1:
            return RSA.generate_private_key(n)
        return (p, q)

    @staticmethod
    def generate_public_key(p, q):
        '''
        Based on the private key, a public key is generated consisting in the pair of numbers (n, e), where:
        - n = p*q
        - e = 65537 (encryption key)    
        '''
        return p*q

    @staticmethod
    def calculate_decryption_exponent(p, q):
        '''
        Calculates d such that ed = 1 (mod φ(n))
        '''
        return modular_division(RSA.e, 1, (p-1)*(q-1))

    def encrypt(self, m):
        '''
        Encrypts message m using public key: c = m^e mod n
        '''
        m_as_int = convert_to_int(m)
        num_bits_of_m = len(binary_expansion(m_as_int))
        if self.num_bits_of_n < num_bits_of_m:
            raise ValueError(f"message too long, num_bits_of_n {self.num_bits_of_n} must be longer than num_bits_of_m {num_bits_of_m}")
        return pow(m_as_int, RSA.e, self.n)

    def decrypt(self, c):
        '''
        Decrypts ciphertext c using decryption key d
        '''
        return convert_to_str(pow(c, self.d, self.n))


def rsa_keys():
    n = 1024
    rsa = RSA(n)
    msg = "hello world, this is an RSA example"

    c = rsa.encrypt(msg)
    print(c)
    print(rsa.decrypt(c))


if __name__ == '__main__':
    rsa_keys()
