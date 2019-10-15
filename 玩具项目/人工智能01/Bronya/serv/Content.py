import os
from flask import Blueprint, jsonify, send_file, request
from Config import RET, MongoDB, COVER_PATH, MUSIC_PATH, LT_URL, QR_PATH

content = Blueprint('content', __name__)

@content.route('/content_list', methods=['post'])
def content_list():
    con_list = list(MongoDB.Content.find({}))  #多个对象返回生成器 循环或者list可直接得到具体结果

    for index, con in enumerate(con_list):
        con_list[index]['_id'] = str(con.get('_id'))  #将数据库的默认id字段 显性加入


    RET['CODE'] = 0
    RET['MSG'] = '获取内容列表'
    RET['data'] = con_list

    return jsonify(RET)


@content.route('/get_cover/<filename>', methods=['get'])
def get_cover(filename):
    file_path = os.path.join(COVER_PATH, filename)
    return send_file(file_path)


@content.route('/get_music/<filename>', methods=['get'])
def get_music(filename):
    file_path = os.path.join(MUSIC_PATH, filename)
    return send_file(file_path)




















