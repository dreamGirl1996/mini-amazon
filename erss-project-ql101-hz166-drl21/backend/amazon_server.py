# from concurrent.futures import ThreadPoolExecutor
from commu_handler import read_serialized_pbuf, send_pbuf
import ups_amazon_pb2 as uapb2
import world_amazon_pb2 as wapb2
import socket
import db_interface
from connect_config import ups_addr, ups_listen_port, world_addr, world_a_port, \
    web_listen_port, amazon_addr, db_host, db_port, world_u_port

from comm_data import Comm_Data, UPS_Comm_Data
import upsConn
import threading
import time
import signal
import sys
import traceback

from utils import global_lock

from world_comm_logic import world_response_handler, send_world_requests, make_pack_requests, create_refill_request

from ups_comm_logic import ups_response_handler, create_val_requests,\
    create_loadfinish_requests, send_ups_requests

import os



class CrashyThread(threading.Thread):
    def run(self):
        try:
            super(CrashyThread, self).run()
        except Exception as e:
            print("error:", e, type(e), file=sys.stderr)
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(e.__traceback__)
            #global_lock.acquire()

            #global_lock.release()
            # traceback.print_tb(exc_traceback, limit=7, file=sys.stderr)
            os._exit(1)


def sig_handler(signal, frame):
    raise db_interface.DBSyntaxError


signal.signal(signal.SIGUSR1, sig_handler)

state_transitions = {
    "pending": "to pack",
    "ready": "load",
    "load": "loaded",
    "loaded": "delivering",
    "delivering": "delivered"
}


def connect_hp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def await_connect(my_addr, port, max_n_unaccepted):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((my_addr, port))
    s.listen(max_n_unaccepted)
    return s


def read_from_world(world_sock, comm_data, u_comm_data):
    # 加锁吗?
    while True:
        serialized = read_serialized_pbuf(world_sock)

        start_thread(lock_function,world_response_handler, serialized, comm_data, u_comm_data)



def read_from_ups(ups_sock, ups_comm_data, world_comm_data):
    while True:
        serialized = read_serialized_pbuf(ups_sock)

        start_thread(lock_function,ups_response_handler, serialized, ups_comm_data, world_comm_data)

'''
def read_from_web(web_sock):
    pass
    '''


def init_warehouses(world_sock, world_id, warehouses):
    AConnect_command = wapb2.AConnect()
    AConnect_command.worldid = world_id
    AConnect_command.isAmazon = True

    for w in warehouses:
        wh_proto = AConnect_command.initwh.add()
        wh_proto.id = w['id']
        wh_proto.x = w['x']
        wh_proto.y = w['y']

    send_pbuf(world_sock, AConnect_command)
    # recv response from world
    AConnected_response = wapb2.AConnected()
    AConnected_response.ParseFromString(read_serialized_pbuf(world_sock))
    print(AConnected_response.result)

    # assert AConnected_response.result == 'connected!'


def get_world_id(ups_sock):
    cmd = uapb2.UtoACommand()

    serialized = read_serialized_pbuf(ups_sock)
    cmd.ParseFromString(serialized)
    UtoAConnect_response = cmd.connection[0]
    world_id = UtoAConnect_response.worldId
    seqnum = UtoAConnect_response.seqNum
    #print(UtoAConnect_response)
    return world_id, seqnum


def periodic_call(delay, func, *args, **kwargs):
    while True:
        global_lock.acquire()
        func(*args, **kwargs)
        global_lock.release()
        time.sleep(delay)

'''
def handle_web(web_accept_sock):
    while True:
        time.sleep(5)
        # print('creating order')
        global_lock.acquire()
        db_interface.create_order()
        global_lock.release()
        # web_sock, addr = web_accept_sock.accept()
        # thread_pool.submit(read_from_web, web_sock)
'''

def start_thread(func, *args,**kwargs):
    t = CrashyThread(target=func, args=args, kwargs=kwargs,daemon=False)
    t.start()

def lock_function(fun,*args,**kwargs):
    global_lock.acquire()
    fun(*args,**kwargs)
    global_lock.release()



def Main():
    web_accept_sock = await_connect(amazon_addr, web_listen_port, 50)
    _ups_accept_sock = await_connect(ups_addr, ups_listen_port, 1)
    print("waiting on ups..")
    ups_sock, _ = _ups_accept_sock.accept()
    w_comm_data, u_comm_data = Comm_Data(), UPS_Comm_Data()
    world_id,seqnum = get_world_id(ups_sock)
    world_sock = connect_hp(world_addr, world_a_port)
    ack_cmd= uapb2.AtoUCommand()
    ack_cmd.ack.append(seqnum)

    send_pbuf(ups_sock,ack_cmd)
    u_comm_data.register_incoming_seqnum(seqnum)

    conn, cur = db_interface.get_db_conn_cursor(db_host, db_port)
    cur.execute('select * from "amazonApp_warehouse";')
    warehouses = cur.fetchall()
    wh_dicts = [{"id": x[0], "x": x[1], "y": x[2]} for x in warehouses]
    conn.close()
    init_warehouses(world_sock, world_id, wh_dicts)
    db_interface.clear_db()

    #conn = psycopg2.connect(dbname="amazondb", user="postgres", host=db_host, port=db_port, password="password")


    try:
        start_thread(read_from_world, world_sock, w_comm_data, u_comm_data)
        start_thread(periodic_call, 3, send_world_requests, world_sock, w_comm_data)
        start_thread(periodic_call, 0.5, make_pack_requests, w_comm_data)
        start_thread(periodic_call, 3.5, create_refill_request, w_comm_data, 1000)

        start_thread(read_from_ups, ups_sock, u_comm_data, w_comm_data)
        start_thread(periodic_call,1,create_val_requests,u_comm_data)
        start_thread(periodic_call, 1, send_ups_requests, ups_sock, u_comm_data)
        start_thread(periodic_call, 0.5, create_loadfinish_requests, u_comm_data)

        #start_thread(read_from_web,web_accept_sock)
        #start_thread(periodic_call, 10,db_interface.create_order,ups_acc='default')

        while True:
            print('i sleep')
            time.sleep(10000)
            print('real shit?')
    except KeyboardInterrupt:
        print('server finish')
        world_sock.close()
        ups_sock.close()
        web_accept_sock.close()
        sys.exit(1)


# main
if __name__ == '__main__':
    print(get_world_id)
    if len(sys.argv) != 1:
        assert len(sys.argv) == 2 and sys.argv[1] == 'haveups'
        print("use ups")
        Main()
    else:
        print("don't use ups")

        start_thread(upsConn.conn_amazon,
                     world_addr, world_u_port, amazon_addr, ups_listen_port)
        Main()
        # thread_pool.submit(upsConn.conn_amazon, world_addr, world_u_port, amazon_addr, ups_listen_port)

    # thread_pool.shutdown()
