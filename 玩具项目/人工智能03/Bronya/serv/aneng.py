import os
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB
from bson import ObjectId

friends = Blueprint('friends', __name__)


@friends.route('/friend_list', methods=['post'])
def friend_list():
    user_id = request.form.get('_id')
    user_info = MongoDB.user.find_one({'_id': ObjectId(user_id)})

    RET['CODE'] = 0
    RET['MSG'] = '好友查询'
    RET['DATA'] = user_info.get('friend_list')

    return jsonify(RET)


@friends.route('/chat_list', methods=['post'])
def chat_list():
    chat_info = request.form.to_dict()
    chat_id = ObjectId(chat_info.get('chat_id'))
    #查询聊天窗口
    chat_list = MongoDB.Chats.find_one({'_id': chat_id})
    #返回聊天记录
    RET['CODE'] = 0
    RET['MSG'] = '查询聊天记录'
    RET['DATA'] = chat_list.get('chat_list')[-5:]

    return jsonify(RET)