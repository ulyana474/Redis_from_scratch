import logging
import re
import socket
from threading import Thread

from helpers.encode_decode import encode_simple_str, encode_bulk_str

buffer = {}

def process_response(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            else:
                if re.search('echo', data, re.IGNORECASE):
                    data_parts = data.split('\r\n')
                    echo_word = data_parts[-2]
                    client_socket.send(encode_bulk_str(echo_word))
                if 'PING' in data:
                    client_socket.send(encode_simple_str('PONG'))
                if 'SET' in data:
                    data_parts = data.split('\r\n')
                    key = data_parts[4]
                    value = data_parts[6]
                    buffer[key] = value
                    client_socket.send(encode_simple_str('OK'))
                if 'GET' in data:
                    data_parts = data.split('\r\n')
                    key = data_parts[4]
                    returned_value = buffer.get(key)
                    if buffer:
                        client_socket.send(encode_bulk_str((returned_value)))
                    else:
                        logging.log(f'Can not GET value by key {key}')
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        client_socket.close()
        print(f"Connection closed for {addr}")

def main():
    host = "localhost"
    port = 6379

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        print(f"New connection from: {addr}")
        thread = Thread(target=process_response, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
