
import os
from flask import Blueprint, request, jsonify
from Config import RET, QR_PATH, MongoDB
from bson import ObjectId


sbe = Blueprint('sb', __name__)


@sbe.route('/scan_qr', methods=['post'])
def scan_qr():
    res_dic = request.form.to_dict()
    target_qr = res_dic.get('device_key')
    msg = '请扫描玩具二维码'
    data = {}
    for qr in os.listdir(QR_PATH):
        if qr[:-4] == target_qr:
            msg = '二维码扫描成功'
            data = {'device_key': target_qr}
            break

    RET['CODE'] = 0
    RET['MSG'] = msg
    RET['DATA'] = data

    return jsonify(RET)



@sbe.route('/bind_toy', methods=['post'])
def bind_list():
    toy_dict = request.form.to_dict()
    print(toy_dict)
    MongoDB.toy.insert_one(toy_dict)
    RET['CODE'] = 0
    RET['MSG'] = '绑定完成'
    RET['DATA'] = {}

    return jsonify(RET)






@sbe.route('/toy_list',methods=['post'])
def toy_list():
    user_dict = request.form.to_dict()
    toy_info_list = list(MongoDB.toy.find({'user_id': user_dict.get('_id')}))
    #[{'_id': ObjectId('5d555e7d636df5c4b398467f'), 'toy_name': '立兴', 'baby_name': '吾儿奉先',
    # 'remark': 'dad', 'device_key': '1f72629f103ca3ae5b9e0baf943e6d2d', 'user_id': '5d553430c1f95f08080e2bb6'}]

    for toy in toy_info_list:
        toy['avatar'] = 'toy.jpg'
        toy['_id'] = f"ObjectId({str(toy['_id'])})"
        toy['bind_user'] = toy.pop('user_id')
        toy['gender'] = 1
        toy['friend_list'] = []

    RET['CODE'] = 0
    RET['MSG'] = '获取Toy列表'
    RET['DATA'] = toy_info_list

    return jsonify(RET)






