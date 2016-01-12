#!/usr/bin/python
import smbus
import time
import json
import threading
from bottle import request, Bottle, abort, static_file
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


##sockets and webserver functions
app = Bottle()
clients = []

def send_all(msg):
    try:
        for client in clients:
            client.send(msg)
    except:
        pass

@app.route('/')
def handle_site():
    return static_file("index.html", root='./')

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    clients.append(wsock)
    while True:
        try:
            message = wsock.receive()
        except WebSocketError:
            clients.remove(wsock)
            break


def ws():
    server = WSGIServer(("0.0.0.0", 8080), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()
#######

##i2c functions
def read_byte(adr):
    return i2c.read_byte_data(address, adr)

def read_word(adr):
    high = i2c.read_byte_data(address, adr)
    low = i2c.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_with_sign(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
#######

i2c = smbus.SMBus(1) #i2c init
address = 0x68 # chip address
i2c.write_byte_data(address,  0x6b, 0) #turn on accelerometer

##start websocket server
th_server = threading.Thread(target=ws)
th_server.setDaemon(True)
th_server.start()

##accelerometer read
while True:
    accel_xout = read_word_with_sign(0x3b)
    accel_yout = read_word_with_sign(0x3d)
    accel_zout = read_word_with_sign(0x3f)
    print accel_xout, accel_yout, accel_zout
    send_all(json.dumps({"x": accel_xout, "y": accel_yout, "z": accel_zout}))
    time.sleep(0.1) #u can try to send data faster :)
