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
"""
import socket
import threading
import message_parser
from datetime import datetime
import time
import gui

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345


def connect_forever():
    while True:
        if gui.connection_label['text'] == 'Not connected':
            try:
                s.connect(('0.0.0.0', port))
                gui.set_connected()
            except ConnectionRefusedError:
                pass
            except OSError:
                pass
        time.sleep(5)


last_connection_verified = datetime.now().timestamp() - 15


def send(msg):
    s.send(msg.encode())


def receive():
    return s.recv(1024).decode()


def on_new_message(message):
    if message == 'you are connected':
        global last_connection_verified
        last_connection_verified = datetime.now().timestamp()
    else:
        server, channel, incoming_message = message_parser.decode_message(message)


def verify_connection_forever():
    while True:
        try:
            if datetime.now().timestamp() - last_connection_verified > 9:
                gui.set_disconnected()
            else:
                gui.set_connected()
            time.sleep(10)
        except:
            pass


def check_for_new_messages():
    while True:
        try:
            msg = receive()
            if msg == '\n':
                continue
            on_new_message(msg)
        except:
            pass


threading.Thread(target=connect_forever).start()
threading.Thread(target=check_for_new_messages).start()
threading.Thread(target=verify_connection_forever).start()
