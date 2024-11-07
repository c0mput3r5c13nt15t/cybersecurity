# RSA in C

**This is a simple (and very insecure!) implementation of RSA in C. It is not safe to use in production. It is for educational purposes only.**

## Hot to use

Choose two prime numbers `p` and `q`.

```c
const int p = 331;
const int q = 269;
```

Chose a public exponent `e`. It must be coprime with `(p-1)(q-1)`.

```c
unsigned long e = 131;
```

Run the program.

```bash
$ gcc main.c && ./a.out                                                                                                                                                    1 ⨯[7-11-2024|21:36:37]
Public key: (131, 89039)
Private key: (64811, 89039)

Original message: 54321
Encrypted message: 69474
Decrypted message: 54321
```

## Debug

To enable debug mode, define the `DEBUG` macro.

```c
#define DEBUG 1
```