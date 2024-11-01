"""Tests for Chatbox OSC."""

from time import sleep

from chatbox_osc import FONTS, write_chatbox


def test_write_message(client, chatbox_fixture):
    test_message = "This is a test"
    write_chatbox(client, test_message)
    sleep(1.5)
    assert chatbox_fixture.message_input == test_message


def test_write_message_with_font(client, chatbox_fixture):
    test_message = "This is a test"
    for font_name, font_fn in FONTS.items():
        if not font_fn:
            continue
        test_message_with_font = font_fn("This is a test")
        write_chatbox(client, test_message, font=font_name)
        sleep(1.5)
        message_input = chatbox_fixture.message_input
        if font_name == "Wide":
            message_input = message_input.replace(" ", "\u2007")
        assert message_input == test_message_with_font
