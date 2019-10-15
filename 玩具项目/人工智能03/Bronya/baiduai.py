import os
from uuid import uuid4

from Config import CHAT_PATH, AUDIO_CLIENT, VOICE


def text2audio(text):
    filename = f"{uuid4()}.mp3"
    filepath = os.path.join(CHAT_PATH, filename)
    res = AUDIO_CLIENT.synthesis(text, 'zh', 1, VOICE)
    if not isinstance(res, dict):
        with open(filepath, 'wb') as f:
            f.write(res)

    return filename


def audio2text():
    pass


def my_nlp():
    pass
