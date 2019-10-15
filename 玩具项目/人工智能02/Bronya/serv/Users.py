import os

from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH
from bson import ObjectId

user = Blueprint('user', __name__)

@user.route('/reg', methods=['post'])
def reg():
    user_info = request.form.to_dict()
    user_info['avatar'] = 'baba.jpg' if user_info.get('gender') == '2' else 'mama.jpg'
    user_info['bind_toys'] = []
    user_info['friend_list'] = []

    MongoDB.user.insert_one(user_info)

    RET['CODE'] = 0
    RET['MSG'] = '注册成功'
    RET['DATA'] = []

    return jsonify(RET)


@user.route('/login', methods=['post'])
def login():
    user_dict = request.form.to_dict()
    user_info = MongoDB.user.find_one(user_dict, {'password': 0})
    user_info['_id'] = str(user_info.get('_id'))
    # user_info['chat']['count'] = 0
    RET['CODE'] = 0
    RET['MSG'] = '登录成功'
    RET['DATA'] = user_info

    return jsonify(RET)


@user.route('/auto_login', methods=['post'])
def auto_login():
    user_dict = request.form.to_dict()
    user_info_dict = MongoDB.user.find_one({'_id': ObjectId(user_dict.get('_id'))}, {'password': 0})
    # user_info_dict['chat']['count'] = 0
    if user_info_dict:
        user_info_dict['_id'] = str(user_info_dict.pop('_id'))
        RET['CODE'] = 0
        RET['MSG'] = '登录成功'
        RET['DATA'] = user_info_dict

        return RET
    else:
        RET['CODE'] = 999
        RET['MSG'] = '登录失败'












