from concurrent.futures import ThreadPoolExecutor
import socket
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint
import world_ups_pb2 as wupb
import ups_amazon_pb2 as uapb
import time

#host,port for ups to world
from connect_config import world_addr, world_a_port, amazon_addr, ups_listen_port,world_u_port

def upsConnectAmazon(ua_host,ua_port):
    socket_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_id.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_id.connect((ua_host, ua_port))
    print("connect with amazon")
    return socket_id


def upsConnectWorld(uw_host,uw_port):
    socket_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_id.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socket_id.connect((uw_host, uw_port))
    print("connect with world")
    return socket_id

def Send(sock, msg):
    #print('sending out the following: ')
    #print(msg)
    req = msg.SerializeToString()
    _EncodeVarint(sock.send, len(req), None)
    sock.send(req)
    print('send finish')


def URecv(sock, isUConnect=False):
    all_data = b''
    data = sock.recv(4)
    if not data:
        print('connection to world is closed')
    data_len, new_pos = _DecodeVarint32(data, 0)
    all_data += data[new_pos:]

    data_left = data_len - len(all_data)
    while True:
        data = sock.recv(data_left)
        all_data += data
        data_left -= len(data)

        if data_left <= 0:
            break

    if isUConnect:
        msg = wupb.UConnected()
        msg.ParseFromString(all_data)
        return msg

    msg = wupb.UResponses()
    msg.ParseFromString(all_data)
    return msg

def getWorldId(uw_socket,worldId):
    connItem = wupb.UConnect()
    connItem.isAmazon = False
    if worldId == 0:
        num_truck = 100
        # store trucks in database while put it in connMsg
        for i in range(num_truck):
            t = connItem.trucks.add()
            t.id = i
            t.x = 99
            t.y = 99

    if worldId > 0:
        connItem.worldid = worldId

    Send(uw_socket, connItem)

    res = URecv(uw_socket, True)

    print('World connection status: ', res.result)
    return res.worldid

def _conn_amazon(world_addr, world_port, am_addr, am_port):
    print(world_addr, world_u_port)
    uwsocket = upsConnectWorld(world_addr, world_port)
    world_id = getWorldId(uwsocket, 0)
    print(world_id)
    uasocket = upsConnectAmazon(am_addr, am_port)

    sendBuffer = uapb.UtoAConnect()
    sendBuffer.seqNum = 1
    sendBuffer.worldId = world_id
    msg=uapb.UtoACommand()
    msg.connection.append(sendBuffer)
    Send(uasocket, msg)
    return uasocket

import traceback
import time
def conn_amazon(world_addr, world_port, am_addr, am_port):
    time.sleep(2)
    sock = _conn_amazon(world_addr, world_port, am_addr, am_port)
    while True:
        time.sleep(1000)
    '''
    while True:
        try:
           
            while True:
                print(" i sleep")
                time.sleep(10000)

        except Exception as e:
            traceback.print_tb(e.__traceback__)

            pass
    '''


if __name__ == '__main__':
    conn_amazon(world_addr,world_u_port,amazon_addr,ups_listen_port)
