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
import tkinter

import socket_handler
import message_parser
import messages
import gui


class Channel:
    def __init__(self, name):
        self.name = name

    def set(self):
        gui.set_channel_name(self.name)
        gui.clear_messages()
        for message in messages.get_messages():
            if message.server == gui.get_server_name() and message.channel == self.name:
                if message.type_ == "incoming":
                    gui.incoming_message(message.msg)
                elif message.type_ == "outgoing":
                    gui.outgoing_message(message.msg)


class Server:
    def __init__(self, host, port, name, channels: list):
        self.host = host
        self.port = port
        self.name = name

        def on_new_message(channel, message):
            messages.Message(server=self.name, channel=channel, message=message, type_="incoming")
            if self.name == gui.get_server_name() and channel == gui.get_channel_name():
                gui.incoming_message(message)

        self.socket = socket_handler.ServerConnection(self.host, self.port, on_new_message)
        self.channels = channels
        self.send = self.socket.send
        self.button = tkinter.Button

    def set(self):
        gui.set_server_name(self.name)
        gui.set_channels(self.channels)
        self.channels[0].set()

    def configure(self, button):
        self.socket.configure(button)
        self.button = button


servers = [Server("localhost", 1265, "Server 1", [Channel("Channel 1"), Channel("Channel 2")])]
gui.set_servers(servers)
servers[0].set()
servers[0].channels[0].set()


def get_current_server_by_name(name):
    for server in servers:
        if server.name == name:
            return server
    return None


def send_msg(message):
    server = get_current_server_by_name(gui.get_server_name())
    channel = gui.get_channel_name()
    server.send(message_parser.encode_message(channel=channel, message=message))
    messages.Message(server=server.name, channel=channel, message=message, type_="outgoing")


gui.set_send_message_command(send_msg)
gui.set_get_server_by_name_command(get_current_server_by_name)

gui.main()
