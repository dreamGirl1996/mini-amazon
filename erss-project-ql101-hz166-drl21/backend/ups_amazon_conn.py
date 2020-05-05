import socket
# import select                                                                                                                                                                                             
# import psycopg2                                                                                                                                                                                           
import world_amazon_pb2 as wapb2
import backend.ups_amazon_pb2 as uapb2
from google.protobuf.internal.decoder import _DecodeVarint32

def recv_ups(sock):
    buff = []
    while True:
        tmp = sock.recv(1)
        buff += tmp
        msg_len, new_pos = _DecodeVarint32(buff, 0)
        if new_pos != 0:
            break
    msg = sock.recv(msg_len)
    print("receive a msg: ")
    print(msg)
    return msg

# return AResponses                                                                                                                                                                                         
def receive_ups(sock):
    data = recv_ups(sock)
    msg = wapb2.AResponses()
    msg.ParseFromString(data)
    return msg



def amazonWaitUpsID(ahost,upsport):
    s_id = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_id.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s_id.bind((ahost, upsport))
    s_id.listen(100)
    print("amazon listen")

    client_id, client_addr = s_id.accept()

    # recv from ups about worldid                                                                                                                                                                           
    UtoAConnect_response = uapb2.UtoAConnect()
    #UtoAConnect_response.ParseFromString(recv_ups(client_id))                                                                                                                                              
    #world_id = UtoAConnect_response.worldid                                                                                                                                                                
    world_id=client_id.recv(10)
    print(world_id)
    return world_id