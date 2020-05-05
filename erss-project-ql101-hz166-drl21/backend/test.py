from concurrent.futures import ThreadPoolExecutor
from commu_handler import read_serialized_pbuf, send_pbuf
import ups_amazon_pb2 as uapb2
import world_amazon_pb2 as wapb2
import socket
import db_interface
from connect_config import ups_addr, ups_listen_port,world_addr,world_a_port, \
    web_listen_port, amazon_addr, db_host, db_port, world_u_port
import psycopg2
from seqnum_handler import get_seqnum
from comm_data import Comm_Data
import upsConn
import threading
import time
import signal
import sys

thread_pool = ThreadPoolExecutor(max_workers=20)


def heh():
    print('hi')

thread_pool.submit(heh)
thread_pool.submit(heh)
thread_pool.shutdown()
