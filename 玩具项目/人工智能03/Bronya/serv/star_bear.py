
import os
import time

from flask import Blueprint, request, jsonify
from Config import RET, MongoDB
from bson import ObjectId


sbe = Blueprint('sb', __name__)


@sbe.route('/scan_qr', methods=['post'])
def scan_qr():
    res_dic = request.form.to_dict()
    device = MongoDB.devices.find_one(res_dic)   #查找二维码是否在数据库里
    toys = MongoDB.Toys.find_one(res_dic)
    if device:
        #授权成功
        RET['CODE'] = 0
        RET['MSG'] = '二维码扫描成功'
        RET['DATA'] = res_dic
    elif toys:
        #二维码已经进行绑定
        RET['CODE'] = 2
        RET['MSG'] = '设备已经进行绑定'
        RET['DATA'] = {'toy_id': str(toys.get('_id'))}
    else:
        #扫描二维码错误
        RET['CODE'] = 1
        RET['MSG'] = '请扫描玩具二维码'
        RET['DATA'] = {}

    return jsonify(RET)


@sbe.route('/bind_toy', methods=['post'])
def bind_toy():
    '''
    创建玩具 并和app进行绑定
    :return:
    '''
    toy_info = request.form.to_dict()
    toy_info["avatar"] = "toy.jpg"
    toy_info["bind_user"] = toy_info.get("user_id")
    toy_info["friend_list"] = []

    user_id = toy_info.pop('user_id')
    user_info = MongoDB.user.find_one({'_id': ObjectId(user_id)})

    chat_window = MongoDB.Chats.insert_one({'user_list': [], 'chat_list': []})
    chat_id = str(chat_window.inserted_id)

    #创建toy在 friendlist的名片
    toy_add_user = {
        "friend_id": user_id,
        "friend_nick": user_info.get('username'),
        "friend_remark": toy_info.get('remark'),
        "friend_avatar": user_info.get('avatar'),
        "friend_chat": chat_id,
        "friend_type": "app"
    }

    toy_info['friend_list'].append(toy_add_user)


    #创建玩具
    toy = MongoDB.Toys.insert_one(toy_info)
    toy_id = str(toy.inserted_id)

    user_info['bind_toys'].append(toy_id)
    #创建user在  friendlist的名片
    user_add_toy = {
        "friend_id": toy_id,
        "friend_nick": toy_info.get('toy_name'),
        "friend_remark": toy_info.get('baby_name'),
        "friend_avatar": toy_info.get('avatar'),
        "friend_chat": chat_id,
        "friend_type": "toy"
        }
    user_info['friend_list'].append(user_add_toy)

    #更新user
    MongoDB.user.update_one({'_id': ObjectId(user_id)}, {'$set': user_info})

    #聊天窗口
    MongoDB.Chats.update_one({'_id': ObjectId(chat_id)}, {'$set': {'user_list': [toy_id, user_id]}})

    RET['CODE'] = 0
    RET['MSG'] = '绑定完成'
    RET['DATA'] = {}

    return jsonify(RET)

    # # 进行绑定?
    # # 1.玩具不存在 创建玩具
    # # 在数据库中创建一条数据 Toys 数据存储结构
    # toy_info["avatar"] = "toy.jpg"
    # toy_info["bind_user"] = toy_info.pop("user_id")
    # toy_info["friend_list"] = []
    # toy_id = MongoDB.Toys.insert_one(toy_info).inserted_id
    #
    # #已经确定了 user_id和 toy_id 创建聊天表加入
    # chat_dic = {
    #     'user_list': [toy_info.get('user_id'), ],
    #     'chat_list': [user_id, toy_id],
    #     'createTime': time.time()
    # }
    # chat_id = MongoDB.Chats.insert_one(chat_dic).inserted_id
    # toy_dic = MongoDB.Toys.find_one({'_id': ObjectId(toy_id)})
    # t_friend_dict = {
    #                     "friend_id": toy_id,
    #                     "friend_nick": toy_dic.get('toy_name'),
    #                     "friend_remark": toy_dic.get('baby_name'),
    #                     "friend_avatar": toy_dic.get('avatar'),
    #                     "friend_chat": chat_id,
    #                     "friend_type": "toy"
    # }
    # MongoDB.users.update_one({'_id': ObjectId(user_id)}, {'$set': {'friend_list': [t_friend_dict]}})  #更新用户
    # user_dic = MongoDB.users.find_one({'_id': ObjectId(user_id)})
    # u_friend_dict = {
    #     "friend_id": user_id,
    #     "friend_nick": user_dic.get('username'),
    #     "friend_remark": user_dic.get('nickname'),
    #     "friend_avatar": user_dic.get('avatar'),
    #     "friend_chat": chat_id,
    #     "friend_type": "app"
    # }
    # MongoDB.Toys.update_one({'_id': ObjectId(toy_id)}, {'$set': {'friend_list': [u_friend_dict]}})  #用户更新玩具


    # 如果 friend_list 空的 要不要创建 Toy

    # 创建聊天窗口
    # "friend_chat" : "5ca17c7aea512d26281bcb8c",私聊窗口ID
    #  chat_window = MongoDB.Chats.insert_one({user_list:[appid toy_id],chat_list:[]})
    # chat_window.inserted_id ObjectId
    # 如果没有toy_id 能不能创建一个空的 user_list:[]

    # 写入数据库 toy = MongoDB.Toys.insert_one(toy_info) .inserted_id

    # 2.建立和 app的绑定关系 user["bind_toy"]append(toy_id)
    # 1.方式一 查询 用户信息 , 更改用户信息user["bind_toy"]append(toy_id) 更新用户信息update_one
    # 2.方式二 直接更新 用户信息表中的 bind_toy

    # 3.双方的关系 好友通讯录 添加名片 成为好友关系?
    # app 可以与 toy 沟通
    # user[friend_list] toy_info["friend_list"] 互相交换名片?
    # 名片 =  ? user 添加 toy 的名片到 firend_lsit


@sbe.route('/toy_list', methods=['post'])
def toy_list():
    user_id = request.form.get('_id')
    user_bind_toy_list = list(MongoDB.Toys.find({'bind_user': user_id}))

    for index, item in enumerate(user_bind_toy_list):
        user_bind_toy_list[index]['_id'] = str(item.get('_id'))

    RET['CODE'] = 0
    RET['MSG'] = '获取Tony列表'
    RET['DATA'] = user_bind_toy_list

    return jsonify(RET)


@sbe.route('/open_toy', methods=['post'])
def open_toy():
    device_key = request.form.to_dict('device_key')
    exist_status = MongoDB.devices.find_one(device_key)  #判断二维码是否存在
    binding_status = MongoDB.Toys.find_one(device_key)  # 判断二维码是否已经绑定
    print(exist_status, binding_status)
    if binding_status:
        #授权成功
        res = {
            "code": 0,
            "music": "Success.mp3",
            "toy_id": str(binding_status.get('_id')),
            "name": binding_status.get('toy_name')
        }
    elif not binding_status and exist_status:
        #二维码未绑定
        res = {
            "code": 2,
            "music": "Nolic.mp3",
        }
    else:
        #不存在的二维码
        res = {
            "code": 1,
            "music": "Nobind.mp3",
        }

    return jsonify(res)











