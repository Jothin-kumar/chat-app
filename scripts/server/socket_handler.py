"""
MIT License

Copyright (c) 2021 B.Jothin kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Author: Jothin kumar (https://jothin-kumar.github.io)
Repository link: https://github.com/Jothin-kumar/chat-app
"""
import socket
import time
import threading
import message_parser

s = socket.socket()
port = 1265
s.bind(('', port))
s.listen(5)
clients = []


def on_new_message(msg, sender):
    channel, message = message_parser.decode_message(msg)
    for client in clients:
        if client != sender:
            client.send(message_parser.encode_message(channel, message))


def on_new_client(client):
    def send_connected_message():
        while True:
            sleep = True
            try:
                client.send(b'you are connected')
            except BrokenPipeError:
                sleep = False
                time.sleep(1)
            except ConnectionResetError:
                clients.remove(client)
                break
            if sleep:
                time.sleep(10)

    def receive_message():
        while True:
            try:
                message = client.recv(1024)
                if message:
                    on_new_message(message, client)
            except ConnectionResetError:
                clients.remove(client)
                break

    threading.Thread(target=send_connected_message).start()
    threading.Thread(target=receive_message).start()
    clients.append(client)


def start_server():
    while True:
        conn, addr = s.accept()
        print('Got connection from', addr)
        on_new_client(conn)
