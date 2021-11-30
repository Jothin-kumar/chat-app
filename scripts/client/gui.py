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
import tkinter as tk
from tkinter.messagebox import showerror

root = tk.Tk()
root.title("Chat application")
root.minsize(width=1000, height=500)
main = root.mainloop

servers_and_channels = tk.Frame(root, bg='black')
servers = tk.Frame(servers_and_channels, width=25, bg='gray15')


def set_servers(servers_: list):
    for server in servers_:
        button = tk.Button(servers, text=server.name, command=server.set)
        button.pack(side=tk.TOP, anchor=tk.W, padx=20, pady=10)
        server.configure(button)


def get_server_by_name_command(name):
    # Command to get a server object by name. can be set using the set_get_server_by_name_command method.
    pass


def set_get_server_by_name_command(command):
    global get_server_by_name_command
    get_server_by_name_command = command


profile_button = tk.Button(servers, text="Profile", bg='gray15', fg='white', font=('Helvetica', 15))
profile_button.pack(side=tk.TOP, fill=tk.X)
servers.pack(side=tk.LEFT, fill=tk.Y)
channels_frame = tk.Frame(servers_and_channels, width=30, bg='gray17')
channels = []


def set_channels(channel_names_and_command: list):
    global channels
    for channel in channels:
        channel.pack_forget()
    channels = []
    for channel in channel_names_and_command:
        button = tk.Button(channels_frame, text=channel.name, command=channel.set)
        button.pack(side=tk.TOP, anchor=tk.W, padx=20, pady=10, fill=tk.X)
        channels.append(button)


server_name_label = tk.Label(channels_frame, text="Server", bg='gray15', fg='white', font=('Helvetica', 25), width=15)


def set_server_name(text):
    server_name_label.config(text=text)


def get_server_name():
    return server_name_label.cget("text")


server_name_label.pack(side=tk.TOP, fill=tk.X)
channels_frame.pack(side=tk.LEFT, fill=tk.Y)
servers_and_channels.pack(side=tk.LEFT, fill=tk.Y)

message_area = tk.Frame(root)
channel_name_label = tk.Label(message_area, bg='gray20', fg='snow', text="Channel", font=("Helvetica", 25))


def set_channel_name(text):
    channel_name_label.config(text=text)


def get_channel_name():
    return channel_name_label.cget("text")


channel_name_label.pack(side=tk.TOP, fill=tk.X)
chats_frame = tk.Frame(message_area, bg='gray25')
messages_frame = tk.Frame(chats_frame, bg='gray25')
message_labels = []


def incoming_message(message):
    message_label = tk.Label(messages_frame, bg='gray20', fg='snow', text=message, font=("Helvetica", 15))
    message_label.pack(side=tk.TOP, anchor=tk.W, padx=20, pady=10)
    message_labels.append(message_label)


def outgoing_message(message):
    message_label = tk.Label(messages_frame, bg='gray20', fg='snow', text=message, font=("Helvetica", 15))
    message_label.pack(side=tk.TOP, anchor=tk.E, padx=20, pady=10)
    message_labels.append(message_label)


def clear_messages():
    for message_label in message_labels:
        message_label.pack_forget()
    message_labels.clear()


messages_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
send_message_frame = tk.Frame(chats_frame, bg='gray25')
message_input = tk.Entry(send_message_frame, bg='gray30', fg='white', font=("Helvetica", 15))


def on_enter(event):
    send_message()


message_input.bind('<Return>', on_enter)
message_input.pack(side=tk.LEFT, fill=tk.X, expand=True)


def send_message():
    if get_server_by_name_command(get_server_name()).button['bg'] == 'green':
        msg = message_input.get().strip().strip('\n')
        if msg:
            outgoing_message(msg)
            message_input.delete(0, tk.END)
            send_message_command(msg)
    else:
        showerror(
            title='Not connected',
            message='Your message cannot be sent because, you are not connected.'
                    'Please connect to the internet and try again.'
        )


def send_message_command(msg):
    # Command to send a message to the server. can be set using the set_send_message_command method.
    pass


def set_send_message_command(command):
    global send_message_command
    send_message_command = command


send_message_button = tk.Button(send_message_frame, text="Send", bg='gray20', fg='white', font=("Helvetica", 15),
                                command=send_message)
send_message_button.pack(side=tk.LEFT, fill=tk.X, padx=5)
send_message_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=15)
chats_frame.pack(fill=tk.BOTH, expand=True)
message_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
