import re
import socket
from threading import Thread

def on_new_client(client_socket, addr):
    try:
        while True:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break
            else:
                if re.search('echo', data, re.IGNORECASE):
                    data_parts = data.split('\r\n')
                    echo_word = data_parts[-2]
                    resp_bulk_str = f'${len(echo_word)}\r\n{echo_word}\r\n'
                    client_socket.send(resp_bulk_str.encode('utf-8'))
                if data == '*1\r\n$4\r\nPING\r\n':
                    client_socket.send(b'+PONG\r\n')
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
        conn, addr = s.accept()  # wait for client
        print(f"New connection from: {addr}")
        thread = Thread(target=on_new_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    main()
