import random


def encrypt_skytale(plaintext: str, key: int) -> str:
    return "".join(plaintext[i::key] for i in range(key))


def decrypt_skytale(ciphertext: str, key: int) -> str:
    # Calculate the number of rows in the cipher
    num_rows = (len(ciphertext) // key) + 1

    # Calculate the number of empty cells in the last row
    num_empty_cells = (num_rows * key) - len(ciphertext)

    # Create a 2D array to store the characters in the correct positions
    matrix = [["" for _ in range(num_rows)] for _ in range(key)]

    # Fill the last num_empty_cells with the character ' '
    for i in range(num_empty_cells):
        matrix[key - i - 1][-1] = "#"

    # Fill in the matrix with the ciphertext characters
    index = 0
    for i in range(key):
        for j in range(num_rows):
            if matrix[i][j] == "#":
                continue
            matrix[i][j] = ciphertext[index]
            index += 1

    # Read the matrix column by column to get the plaintext
    plaintext = "".join(matrix[i][j] for j in range(num_rows) for i in range(key))

    return plaintext[: len(ciphertext)]


def generate_random_str(length: int) -> str:
    return "".join(
        random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz", k=length)
    )


if __name__ == "__main__":
    assert (
        encrypt_skytale("WICHTIGENACHRICHTENKOMMENMORGEN", 8)
        == "WNTNIAEMCCNOHHKRTROGIIMEGCMNEHE"
    )
    assert (
        decrypt_skytale("WNTNIAEMCCNOHHKRTROGIIMEGCMNEHE", 8)
        == "WICHTIGENACHRICHTENKOMMENMORGEN"
    )

    for i in range(10):
        plaintext = generate_random_str(random.randint(1, 100))
        key = random.randint(1, 100)
        assert decrypt_skytale(encrypt_skytale(plaintext, key), key) == plaintext
