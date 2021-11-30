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
import tkinter


class ServerConnection:
    def __init__(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.button = tkinter.Button
        self.last_connection_verified = datetime.now().timestamp() - 15
        threading.Thread(target=self.connect_forever).start()
        threading.Thread(target=self.check_for_new_messages).start()
        threading.Thread(target=self.verify_connection_forever).start()

    def configure(self, button):
        self.button = button
        self.button['bg'] = 'yellow'

    def connect_forever(self):
        while True:
            try:
                if self.button['bg'] == 'yellow':
                    self.socket.connect((self.host, self.port))
                    self.button['bg'] = 'green'
            except ConnectionRefusedError:
                pass
            except OSError:
                pass
            except TypeError:
                pass
            except RuntimeError:
                break
            time.sleep(10)

    def send(self, msg):
        message_sent = False
        while not message_sent:
            try:
                self.socket.send(msg.encode())
                message_sent = True
            except BrokenPipeError:
                self.socket.close()
                self.button['bg'] = 'yellow'
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.host, self.port))
                self.button['bg'] = 'green'

    def receive(self):
        return self.socket.recv(1024).decode()

    def on_new_message(self, message):
        if message == 'you are connected':
            self.last_connection_verified = datetime.now().timestamp()
        else:
            server, channel, incoming_message = message_parser.decode_message(message)

    def verify_connection_forever(self):
        while True:
            try:
                if datetime.now().timestamp() - self.last_connection_verified > 9:
                    self.button['bg'] = 'yellow'
                    try:
                        self.socket.connect((self.host, self.port))
                        self.button['bg'] = 'green'
                    except ConnectionRefusedError:
                        pass
                    except OSError:
                        self.button['bg'] = 'green'
                else:
                    self.button['bg'] = 'green'
                time.sleep(10)
            except RuntimeError:
                break
            except:
                pass

    def check_for_new_messages(self):
        while True:
            try:
                msg = self.receive()
                if msg == '\n':
                    continue
                self.on_new_message(msg)
            except RuntimeError:
                break
            except:
                pass
