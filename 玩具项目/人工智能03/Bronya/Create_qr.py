
import time, hashlib, requests, os
from Config import QR_PATH, LT_URL, MongoDB
from uuid import uuid4


def create_qr(n):
    device_list = []
    for i in range(n):
        salt = hashlib.md5(f"{uuid4()}{time.time()}{uuid4()}".encode('utf-8')).hexdigest()
        qr_res = requests.get(f"{LT_URL}{salt}")
        qr_name = f"{salt}.jpg"
        path = os.path.join(QR_PATH, qr_name)
        with open(path, 'wb')as f:
            f.write(qr_res.content)

        device_key = {
            'device_key': salt
        }
        device_list.append(device_key)

    MongoDB.devices.insert_many(device_list)


create_qr(10)
