import os
import time
from uuid import uuid4
from flask import Blueprint, jsonify, request
from Config import RET, MongoDB, CHAT_PATH
from baiduai import text2audio
from bson import ObjectId

uploader = Blueprint('uploader', __name__)


@uploader.route('/app_uploader', methods=['post'])
def app_uploader():

    app_info = request.form.to_dict()
    user_list = [app_info.get('user_id'), app_info.get('to_user')]
    # 通过 user_list 子集查询 $all  可以获取到 当前的聊天窗口 如果查询的话,会将所有的聊天数据全部查询到,能不能不查询直接更新数据呢?
    # chat_window = MongoDB.Chats.find_one({'user_list': {'$all': user_list}})
    # 获取文件数据 request.files
    file = request.files.get('reco_file')
    # print(request.files)
    # 保存文件 .amr
    filepath = os.path.join(CHAT_PATH, file.filename)
    file.save(filepath)
    # amr 浏览器无法播放  转换成 MP3 - ffmpeg -i amr mp3
    os.system(f'ffmpeg -i {filepath} {filepath[:-4]}.mp3')
    # 删除 amr 的原始文件
    os.remove(f'{filepath}')
    # 创建聊天记录信息 MongoDB数据存储结构文档中查询
    chat_info = {
        "from_user": app_info.get('user_id'),
        "to_user": app_info.get('to_user'),
        "chat": f"{file.filename[:-4]}.mp3",
        "createTime": time.time()
    }
    # 更新chat_list 数据
    MongoDB.Chats.update_one({'user_list': {'$all': user_list}}, {'$push': {'chat_list': chat_info}})

    # 返回给提示用户有信息

    send_info = MongoDB.user.find_one({'_id': ObjectId(app_info.get('user_id'))})
    for item in send_info.get('friend_list'):
        if item['friend_id'] == app_info.get('to_user'):
            message = text2audio(f'你有来自{item["friend_remark"]}的消息')
            break

    # RET 响应数据
    RET['CODE'] = 0
    RET['MSG'] = '上传成功'
    RET['DATA'] = {
        'filename': message,
        'friend_type': 'app'
    }

    return jsonify(RET)


@uploader.route('/toy_uploader', methods=['post'])
def toy_uploader():
    uuid_name = str(uuid4())
    uu_path = os.path.join(CHAT_PATH, uuid_name)
    toy_info = request.form.to_dict()
    user_info = [toy_info.get('user_id'), toy_info.get('to_user')]
    # #通过userid 和to_user 查找 聊天记录
    # user_list = MongoDB.Chats.find_one({'user_list': {'$all': user_info}})
    # #文件数据查找保存
    file = request.files.get('reco')
    # # 保存文件 .amr
    filepath = os.path.join(CHAT_PATH, file.filename)
    file.save(filepath)
    # amr 浏览器无法播放  转换成 MP3 - ffmpeg -i amr mp3
    os.system(f'ffmpeg -i {filepath} {uu_path}.mp3')
    # 删除 amr 的原始文件
    os.remove(f'{filepath}')


    # chat_list = {}
    chat_list = {
        "from_user": toy_info.get('user_id'),
        "to_user": toy_info.get('to_user'),
        "chat": f"{uuid_name}.mp3",
        "createTime": time.time()
    }
    # 更新chat_list 数据
    MongoDB.Chats.update_one({'user_list': {'$all': user_info}}, {'$push': {'chat_list': chat_list}})
    # RET 返回值
    # JSON:
    ret = {
        "code": 0,
        "msg": "上传成功",
        "data":
            {
                "filename": f"{uuid_name}.mp3",
                "friend_type": "toy"
            }
    }

    return jsonify(ret)


@uploader.route('/recv_msg', methods=['post'])
def recv_msg():
    person_info = request.form.to_dict()
    user_list = [person_info.get('from_user'), person_info.get('to_user')]
    res_list = MongoDB.Chats.find_one({'user_list': {'$all': user_list}}, {'to_user': 0})

    chat_window = res_list.get('chat_list')[-1:]

    #修改 格式
    for item in chat_window:
        item['message'] = item.pop('chat')

    return jsonify(chat_window)

