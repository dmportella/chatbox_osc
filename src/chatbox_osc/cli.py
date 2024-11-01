"""Console script for Chatbox OSC."""

import argparse

from pythonosc.udp_client import SimpleUDPClient

from chatbox_osc import write_chatbox


def main_cli() -> None:
    """Console script for Chatbox OSC."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--msg",
        type=str,
        help="The text to be displayed in the Chatbox. "
        "If not provided, the current message will be cleared from the Chatbox.",
    )
    parser.add_argument(
        "-d",
        "--delay",
        type=float,
        default=0,
        help="An optional delay before starting writing in the Chatbox (0 by default) "
        "which creates the '3 dots' typing animation.",
    )
    parser.add_argument(
        "-cl",
        "--chunk-length",
        type=int,
        default=25,
        help="The number of characters per segment for displaying the message "
        "as it is being typed-in. Set to 0 or None to disable this feature "
        "and show the full message at once.",
    )
    parser.add_argument(
        "-f",
        "--font",
        type=str,
        default="Normal",
        help="The name of a predefined text style from FONTS (default: 'Normal') "
        "to be used for the message.",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=9000,
        help="Port number for VRChat OSC (default is 9000).",
    )
    args = parser.parse_args()
    client = SimpleUDPClient("127.0.0.1", args.port)
    write_chatbox(client, args.msg, args.delay, args.chunk_length, args.font)
