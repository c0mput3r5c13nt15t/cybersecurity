import itertools
import random


def generate_password(charset, length):
    return "".join(random.choice(charset) for _ in range(length))


def check_password(password, guess):
    return password == guess


def crack_password(password, charset, max_len=32, verbose=False):
    for length in range(max_len):
        for guess in itertools.product(charset, repeat=length):
            guess = "".join(guess)
            if verbose:
                print("Guessing '", guess, "'", sep="")
            if check_password(password, guess):
                return guess


if __name__ == "__main__":
    charset = "abcdefghijklmnopqrstuvwxyz1234567890"
    password = generate_password(charset, 6)
    print("Genrated password '", password, "'", sep="")
    guess = crack_password(password, charset)
    print("Brute forced password '", guess, "'", sep="")
