#include <stdio.h>
#include <stdbool.h>
#include <assert.h>
#include <stdlib.h>

unsigned long iteratedSquaring(unsigned long x, unsigned long A, unsigned long B);
unsigned long decrypt(unsigned long c, unsigned long d, unsigned long N);
unsigned long calcD(unsigned long e, unsigned long M);
long gcd(unsigned long a, unsigned long b);
bool isPrime(unsigned long n);
void decToBinary(char *binaryNumBuf, unsigned long n);

int main(void)
{
    const int p = 331;
    const int q = 269;

    assert(p != q);
    assert(isPrime(p)); // p must be prime
    assert(isPrime(q)); // q must be prime

    unsigned long N = p * q; // modulus

    unsigned long M = (p - 1) * (q - 1); // Euler's totient function

    unsigned long e = 131; // public key

    assert(gcd(e, M) == 1); // e and M must be coprime

    unsigned long d = calcD(e, M); // private key

    #ifdef DEBUG
    printf("p: %d\n", p);
    printf("q: %d\n", q);
    printf("N: %d\n", N);
    printf("M: %d\n", M);
    printf("e: %d\n", e);
    printf("d: %d\n", d);
    printf("\n");
    #endif // DEBUG

    printf("Public key: (%d, %d)\n", e, N);
    printf("Private key: (%d, %d)\n", d, N);
    printf("\n");

    unsigned long m = 54321; // message

    unsigned long c = iteratedSquaring(m, e, N); // encrypted message

    unsigned long m2 = iteratedSquaring(c, d, N); // decrypted message

    printf("Original message: %d\n", m);
    printf("Encrypted message: %d\n", c);
    printf("Decrypted message: %d\n", m2);

    assert(m == m2);
}

unsigned long iteratedSquaring(unsigned long x, unsigned long n, unsigned long m) // x^n mod m
{
    char binaryNumBuf[sizeof(unsigned long)*8] = {0};
    unsigned long results[sizeof(unsigned long)*8] = {0};
    int c = 1;

    decToBinary(binaryNumBuf, n);

    for (int i = 0; i < sizeof(unsigned long)*8; i++)
    {
        if (binaryNumBuf[i] == 1)
        {
            results[i] = x;
            for (int j = 0; j < sizeof(unsigned long)*8 - 1 - i; j++)
            {
                results[i] = (results[i] * results[i]) % m; // square and then take mod m to keep the numbers small
            }
        }
    }

    for (int i = 0; i < sizeof(unsigned long)*8; i++)
    {
        if (results[i] != 0)
        {
            c = (c * results[i]) % m;
        }
    }

    return c;
}

void decToBinary(char *binaryNumBuf, unsigned long n)
{
    // array to store binary number
    char binaryNumRev[sizeof(unsigned long)*8] = {0};

    // counter for binary array
    int i = 0;
    while (n > 0)
    {
        // storing remainder in binary array
        binaryNumRev[i] = n % 2;
        n = n / 2;
        i++;
    }

    // reverse the binary array (dont print)
    for (int j = sizeof(unsigned long)*8 - 1; j >= 0; j--)
    {
        binaryNumBuf[sizeof(unsigned long)*8 - 1 - j] = binaryNumRev[j];
    }
}

bool isPrime(unsigned long n)
{
    if (n <= 1)
    {
        return false;
    }

    for (int i = 2; i < n; i++)
    {
        if (n % i == 0)
        {
            return false;
        }
    }

    return true;
}

long gcd(unsigned long a, unsigned long b) {
    if (b == 0) {
        return a;
    }

    return gcd(b, a % b);
}

/*
 * Calculate the private key d using the extended Euclidean algorithm
 */
unsigned long calcD(unsigned long e, unsigned long M)
{
    unsigned long old_r = M;
    unsigned long r = e;
    signed long old_s = 1;
    signed long s = 0;
    signed long old_t = 0;
    signed long t = 1;

    signed long temp;
    unsigned long q;
    signed long d; // the result of the algorithm might be negative -> later fixed by adding M

    while (r != 0) {
        q = old_r / r;

        temp = r;
        r = old_r - q * r;
        old_r = temp;

        temp = s;
        s = old_s - q * s;
        old_s = temp;

        temp = t;
        t = old_t - q * t;
        old_t = temp;
    }

    #ifdef DEBUG
    printf("Bézout coefficients: %d, %d\n", old_s, old_t);
    printf("greatest common divisor: %d\n", old_r);
    printf("quotients by the gcd: %d, %d\n", t, s);
    #endif // DEBUG

    if (abs(t) == e) {
        d = old_s;
    } else {
        d = old_t;
    }

    if (d < 0)
    {
        assert((d + M) * e % M == 1);
        return d + M;
    } else {
        assert(d * e % M == 1);
        return d;
    }
}