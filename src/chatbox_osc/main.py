"""Write a message to the VRChat Chatbox, with optional parameters for delay, chunk length, and font style."""

from __future__ import annotations

from time import sleep
from typing import TYPE_CHECKING

import fancify_text
import uwuify

if TYPE_CHECKING:
    from pythonosc.udp_client import SimpleUDPClient


FONTS = {
    "Normal": None,
    "Wide": fancify_text.wide,
    "SmallCaps": fancify_text.smallCaps,
    "Squared": fancify_text.squared,
    "Circled": fancify_text.circled,
    "Parenthesized": fancify_text.parenthesized,
    "Boxed": fancify_text.boxed,
    "Blue": fancify_text.blue,
    "HeavyCircled": fancify_text.heavyCircled,
    "Curly": fancify_text.curly,
    "Currency": fancify_text.currency,
    "Magic": fancify_text.magic,
    "Wiry": fancify_text.wiry,
    "UpsideDown": fancify_text.upsideDown,
    "Superscript": fancify_text.superscript,
    "UwU": None,
}

CHATBOX_MAXIMUM_LENGTH = 144
CHATBOX_UPDATES_DELAY = 1.5  # 1.5sec is the minimum delay between every Chatbox updates in VRC


def write_chatbox(
    client: SimpleUDPClient,
    message: str | None = None,
    delay: float = 0,
    chunk_length: int = 25,
    font: str | None = "Normal",
) -> None:
    """Write a message to the VRChat Chatbox with optional formatting and animation.

    Parameters
    ----------
    client : pythonosc.udp_client.SimpleUDPClient
        The Python OSC client object for sending messages to the Chatbox.
    message : str, optional
        The text to be displayed in the Chatbox.
        If not provided, the current message will be cleared from the Chatbox.
    delay : float, optional
        An optional delay before starting writing in the Chatbox (0 by default)
        which creates the "3 dots" typing animation.
    chunk_length : int, optional
        The number of characters per segment for displaying the message
        as it is being typed-in. At the end of the typing animation,
        this will trigger the Chatbox SFX.
        Set to 0 or None to disable this feature and show the full message at once.
    font : Optional[str], optional
        The name of a predefined text style from FONTS (default: "Normal")
        to be used for the message.
    """
    if not message:  # Clear the current message from the Chatbox
        client.send_message("/chatbox/input", ["", True])
        return
    if delay:  # Create the "3 dots" typing animation
        client.send_message("/chatbox/typing", True)
        sleep(delay)
    message = text_with_font(message, font)
    message_parts = split_into_chunks(message, CHATBOX_MAXIMUM_LENGTH)
    for message_part in message_parts:
        message_generating = ""
        if chunk_length:  # Write the message with a "typing" animation, like ChatGPT
            message_chunk = split_into_chunks(message_part, chunk_length)
            for chunk in message_chunk:
                client.send_message("/chatbox/input", [f"{message_generating}{chunk}■", True, False])
                message_generating += f"{chunk} "
                sleep(CHATBOX_UPDATES_DELAY)
        client.send_message("/chatbox/input", [f"{message_part}", True, bool(chunk_length)])
        if len(message_parts) > 1:
            sleep(CHATBOX_UPDATES_DELAY)
    client.send_message("/chatbox/typing", False)


def text_with_font(text: str, font: str) -> str:
    """Apply a predefined text style to the message.

    Parameters
    ----------
    text : str
        The text to which a font style is applied.
    font : str
        Name of a predefined text style from `FONTS`.

    Returns
    -------
    str
        The input string with applied formatting.
    """
    if font_fn := FONTS.get(font):  # Apply a text style to the message
        text = font_fn(text)
    elif font == "UwU":
        if "?" not in text or "!" not in text:
            text = f"{text}."  # Add dot at the end of the message to add emoji from uwufy
        text = uwuify.uwu(text, flags=uwuify.SMILEY | uwuify.STUTTER)
    return text


def split_into_chunks(text: str, chunk_length: int) -> list[str]:
    """Split a text into chunks of equal or lesser length.

    Each chunk is added to the output list only when its max size
    (including spaces and punctuation as necessary) exceeds the given 'chunk_length'.
    A new chunk starts with any word that would exceed this limit,
    thus ensuring each chunk's length fits within boundaries.

    Parameters
    ----------
    text : str
        The input string to be split into chunks. This should contain words separated by spaces.

    chunk_length : int
        Maximum number of characters allowed in each chunk, including space and punctuation.

    Returns
    -------
    list of str
        A list containing the input text split into chunks of equal or lesser length as
        specified by 'chunk_length'.
        The last element may be shorter if it exceeds the chunk limit, but will never exceed that size.

    Examples
    --------
    >>> split_into_chunks("This is a sample text.", 10)
    ["This is", "a sample", "text."]
    """
    words = text.split()  # Split the text into words
    chunks = []
    current_chunk = ""
    for word in words:
        if len(current_chunk) + len(word) <= chunk_length:
            # If adding this word will not exceed the desired length, add it to the current chunk
            current_chunk += f"{word} "
        else:
            chunks.append(current_chunk.strip())  # Otherwise, start a new chunk with this word
            current_chunk = f"{word} "
    if current_chunk:  # Append the last chunk to the list
        chunks.append(current_chunk.strip())
    return chunks
