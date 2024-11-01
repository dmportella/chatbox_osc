import threading

import pytest
from pythonosc import osc_server
from pythonosc.dispatcher import Dispatcher
from pythonosc.udp_client import SimpleUDPClient


class Chatbox:
    def __init__(self):
        self.message_input = None
        self.message_typing = False

    def set_message_input(self, adress, message, *args):
        self.message_input = message

    def set_message_typing(self, adress, message, *args):
        self.message_typing = message


chatbox = Chatbox()
dispatcher = Dispatcher()
dispatcher.map("/chatbox/input", chatbox.set_message_input)
dispatcher.map("/chatbox/typing", chatbox.set_message_typing)
server = osc_server.ThreadingOSCUDPServer(("127.0.0.1", 9000), dispatcher)


@pytest.fixture()
def client():
    return SimpleUDPClient("127.0.0.1", 9000)


@pytest.fixture(scope="session")
def chatbox_fixture():
    yield chatbox


def server_thread():
    server.serve_forever()


def pytest_sessionstart(session):
    thread = threading.Thread(target=server_thread)
    thread.start()


def pytest_sessionfinish(session, exitstatus):
    server.shutdown()
