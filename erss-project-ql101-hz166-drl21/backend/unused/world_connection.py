import socket
# import select
# import psycopg2
import world_amazon_pb2 as wapb2
from google.protobuf.internal.decoder import _DecodeVarint32
from google.protobuf.internal.encoder import _EncodeVarint

ahost='vcm-8302.vm.duke.edu'
upsport=6666
world_addr = 'vcm-8302.vm.duke.edu'
world_port = 23456




def world_connect(world_addr, world_port, world_id,warehouses):
    AConnect_command = wapb2.AConnect()
    AConnect_command.worldid = world_id
    AConnect_command.isAmazon = True

<<<<<<< HEAD:backend/world_connection.py
<<<<<<< HEAD
def world_connect(world_addr, world_port, world_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
=======
=======
>>>>>>> 356bd9c2d5fbe0693d181b6fe514bbdbe6abaf76:backend/unused/world_connection.py
    for w in warehouses:
        wh_proto = AConnect_command.initwh.add()
        wh_proto.id = w['id']
        wh_proto.x = w['x']
        wh_proto.y = w['y']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
<<<<<<< HEAD:backend/world_connection.py
>>>>>>> fd6c319ed98facfed1fb9babc45e30b93d76d289
    s.connect((world_addr, world_port))
    print('connect to world')
    # constrcut AConnect command
<<<<<<< HEAD
    AConnect_command = wapb2.AConnect()
    AConnect_command.worldid = world_id
    AConnect_command.isAmazon = True
=======


>>>>>>> fd6c319ed98facfed1fb9babc45e30b93d76d289
    # send AConnect to world
=======

    s.connect((world_addr, world_port))
    print('connect to world')
    # constrcut AConnect command
>>>>>>> 356bd9c2d5fbe0693d181b6fe514bbdbe6abaf76:backend/unused/world_connection.py
    send(s, AConnect_command , 'send Aconnect to world')
    # recv response from world
    AConnected_response = wapb2.AConnected()
    AConnected_response.ParseFromString(recv(s))
    worldid = AConnected_response.worldid
    result = AConnected_response.result
    print("Worldid: ")
    print(worldid)
    print("\n")
    print("Result: ")
    print(result)
    print("\n")
    return s



def send(sock, msg, des):
    print("send : ")
    print(msg)
    print(des)
    req = msg.SerializeToString()
    _EncodeVarint(sock.send, len(req), None)
    sock.send(req)
    print('send finish')





def recv(sock):
    # buf = []
    # n = 0
    # while n < len(buf):
    #     msg_len, new_pos = _DecodeVarint32(buf, n)
    #     n = new_pos
    #     msg_buf = buf[n:n+msg_len]
    #     n += msg_len
    #     read_metric = metric_pb2.Metric()
    #     read_metric.ParseFromString(msg_buf)
    buff = []
    while True:
        tmp = sock.recv(1)
        buff += tmp
        msg_len, new_pos = _DecodeVarint32(buff, 0)
        if new_pos != 0:
            break
    #should socket be replaced with sock?
    msg = sock.recv(msg_len)
    print("receive a msg: ")
    print(msg)
    return msg


# return AResponses
def receive_world(sock):
    data = recv(sock)
    msg = wapb2.AResponses()
    msg.ParseFromString(data)
    return msg

# send ARequest to world
def send_world(sock):
    pass


# def Main():

#     # ups 连 amazon 发 wold_id 
#     #serversocket_id=amazonWaitUps(ahost,upsport)
    
#     socket_w = world_connect(world_addr, world_port)

#     socket_w.close()



# if __name__ == "__main__":
#     Main()