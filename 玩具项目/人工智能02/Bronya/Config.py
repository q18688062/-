
from pymongo import MongoClient

MC = MongoClient("127.0.0.1", 27017)
MongoDB = MC["Teresa"]
COVER_PATH = 'Cover'
MUSIC_PATH = 'Music'
QR_PATH = 'QR code'
LT_URL = "http://qr.liantu.com/api.php?text="

RET = {
    'CODE': 0,
    'MSG': '',
    'DATA': {}
}