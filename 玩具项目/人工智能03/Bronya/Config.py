
from pymongo import MongoClient
from aip import AipSpeech

MC = MongoClient("127.0.0.1", 27017)
MongoDB = MC["Teresa"]
COVER_PATH = 'Cover'
MUSIC_PATH = 'Music'
CHAT_PATH = 'Chat'
QR_PATH = 'QR code'
LT_URL = "http://qr.liantu.com/api.php?text="

APP_ID = '16981699'
API_KEY = '36Lnn4w8Yov91xN1B0RXzk8Y'
SECRET_KEY = 'fVqFeNIUKSLO6STTCqeHip8DYMtBvtPz'
AUDIO_CLIENT = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
VOICE = {'vol': 5}

RET = {
    'CODE': 0,
    'MSG': '',
    'DATA': {}
}