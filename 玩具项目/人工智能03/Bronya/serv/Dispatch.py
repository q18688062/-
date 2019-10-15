import json

from geventwebsocket.handler import WebSocketHandler
from geventwebsocket.server import WSGIServer
from geventwebsocket.websocket import WebSocket
from flask import Flask, request


ws_app = Flask(__name__)


user_socket_dict = {}


@ws_app.route('/toy/<toy_id>')
def toy(toy_id):
    user_socket = request.environ.get('wsgi.websocket')# type: WebSocket
    if user_socket:
        user_socket_dict[toy_id] = user_socket

    while True:
        print(user_socket_dict)
        user_msg = user_socket.receive()
        user_msg_dict = json.loads(user_msg)
        receive_id = user_msg_dict.get('to_user')
        receive_socket = user_socket_dict.get(receive_id)
        receive_socket.send(user_msg)


@ws_app.route('/app/<user_id>')
def app(user_id):
    user_socket = request.environ.get('wsgi.websocket')# type: WebSocket
    if user_socket:
        user_socket_dict[user_id] = user_socket

    while True:
        user_msg = user_socket.receive()
        user_msg_dict = json.loads(user_msg)
        receive_id = user_msg_dict.get('to_user')
        receive_socket = user_socket_dict.get(receive_id)
        receive_socket.send(user_msg)








if __name__ == '__main__':
    http_serv = WSGIServer(('0.0.0.0', 9528), ws_app, handler_class=WebSocketHandler)
    http_serv.serve_forever()









