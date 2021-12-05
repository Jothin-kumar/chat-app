messages = []


class Message:
    def __init__(self, message, server, channel, type_='incoming'):
        self.msg = message
        self.server = server
        self.channel = channel
        self.type_ = type_
        messages.append(self)


def get_messages():
    return messages
