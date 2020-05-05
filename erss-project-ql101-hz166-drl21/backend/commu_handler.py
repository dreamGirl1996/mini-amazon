import socket
# import select
# import psycopg2
import world_amazon_pb2 as wapb
import ups_amazon_pb2 as uapb
import web_amazon_pb2 as webamazonpb
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

# 序列号要加锁

# send msg (msg should be constructed before sending)

def read_serialized_pbuf(world_socket):
    try:
        msg_chunk = world_socket.recv(100, socket.MSG_PEEK)
        var_int_buff = list(msg_chunk)
        msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
        world_socket.recv(new_pos,socket.MSG_WAITALL)
        return world_socket.recv(msg_len,socket.MSG_WAITALL)
        '''
        while True:
            buf = world_socket.recv(1)
            var_int_buff += buf
            msg_len, new_pos = _DecodeVarint32(var_int_buff, 0)
            if True:#new_pos != 0:
                break
        whole_message = world_socket.recv(msg_len)
        return whole_message
        '''
    except IndexError as e:
        print("error on socket read. buffer contents:",var_int_buff)
        print(world_socket.recv(1000))
        raise e


def send_pbuf(sock,pbuf):
    req = pbuf.SerializeToString()
    _EncodeVarint(sock.send, len(req), None)
    sock.send(req)
'''
def read_serialized_pbuf(sock):
    buff = []
    try:
        while True:
            tmp = sock.recv(1)
            buff += tmp
            msg_len, new_pos = _DecodeVarint32(buff, 0)
            if new_pos != 0:
                break
        #should socket be replaced with sock?
        msg = sock.recv(msg_len)
        return msg
    except IndexError as e:
        print(buff)
        raise e
'''