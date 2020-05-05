import psycopg2
import os,signal
import code
import threading
from connect_config import db_host, db_port

inventory_lock = threading.Lock()
requesting_inventory= False


ORDER_TABLE = '"amazonApp_order"'
PRODUCTS = '"amazonApp_amazonproduct"'
WAREHOUSES = '"amazonApp_warehouse"'
WAREHOUSE_CONTENTS = '"amazonApp_warehousecontents"'
AUTH_USER = '"auth_user"'

from collections import defaultdict


db_lock = threading.Lock()
class DBSyntaxError(Exception):
    pass

class NoInventoryError(Exception):
    pass


def get_results(cursor):
    try:
        return cursor.fetchall()
    except psycopg2.ProgrammingError as e:
        raise e

        #return []



def get_db_conn_cursor(db_host, db_port):
    conn = psycopg2.connect(dbname="amazondb", user="postgres", host=db_host, port=db_port, password="password")

    return conn, conn.cursor()

conn,cur=get_db_conn_cursor(db_host, db_port)

def distance(x1,x2,y1,y2):
    return (x1-x2)**2+(y1-y2)**2

def get_prodids():
    ex_wrapper(cur,f"select prod_id from {PRODUCTS};")
    ret = cur.fetchall()
    return [x[0] for x in ret]

def get_whids():
    ex_wrapper(cur,f"select wh_id from {WAREHOUSES};")
    ret = cur.fetchall()
    return [x[0] for x in ret]




def get_matching_wh(x,y):
    ex_wrapper(cur,f"select * from {WAREHOUSES};")
    warehouses = cur.fetchall()

    best_wh = None
    shortest_distance = None
    for idx, w in enumerate(warehouses):

        wh_id, wh_x, wh_y = w
        n_dist = distance(wh_x,x,wh_y,y)
        if idx==0 or n_dist<shortest_distance:
            shortest_distance=n_dist
            best_wh=wh_id
    return best_wh

def get_matching_prodid(prod_name):
    ex_wrapper(cur,f"select prod_id from {PRODUCTS} where product_name = '{prod_name}';")
    x= cur.fetchall()
    try:
        assert len(x)==1
    except Exception as e:
        print(x)
        raise e
    return x[0][0]

def get_prod_desc(prodid):
    query = f"select product_desc from {PRODUCTS} where prod_id = %s;"
    ex_wrapper(cur,query,(prodid,))
    ret= cur.fetchone()
    return ret[0]

def ex_wrapper(cur,command,args=None):

    return cur.execute(command,args)


def create_order(uid=1,product_name = 'apple',buyer_x=50, buyer_y=50,time='2010-1-1',
                 product_num=2,ups_acc=None):
    #import pdb; pdb.set_trace()
    if ups_acc:
        status = 'await_valid'
        ex_wrapper(cur,f"INSERT INTO {ORDER_TABLE} (user_id_id, product_name,buyer_x,buyer_y,"
                    f"order_created_time, product_num, status,ups_id) VALUES  "
                    "(%s, %s, %s, %s, %s, %s, %s, %s);",
                    ( uid,product_name,buyer_x,buyer_y,time,product_num,status,ups_acc))
    else:
        status = 'pending'
        ex_wrapper(cur,f"INSERT INTO {ORDER_TABLE} (user_id_id, product_name,buyer_x,buyer_y,"
                    f"order_created_time, product_num, status) VALUES  "
                    "(%s, %s, %s, %s, %s, %s, %s);",
                    ( uid,product_name,buyer_x,buyer_y,time,product_num,status))

    conn.commit()




def increment_inventory(whid, prodid, n):
    #print("args:", whid, prodid, n)
    inventory_lock.acquire()
    ex_wrapper(cur,f"select product_quantity from {WAREHOUSE_CONTENTS} where wh_id_id = %s and prod_id_id = %s;", (whid, prodid))
    ret = get_results(cur)
    #ret = cur.fetchall()
    if not ret:
        ex_wrapper(cur,f"INSERT INTO {WAREHOUSE_CONTENTS} (wh_id_id, prod_id_id, product_quantity) "
                       f"VALUES (%s,%s,0);", (whid, prodid))
        cnt =0
    else:
        assert len(ret)==1
        cnt= ret[0][0]

    ncnt = cnt + n
    if ncnt >=0:
        ex_wrapper(cur,f"UPDATE {WAREHOUSE_CONTENTS} set product_quantity = %s "
                       f"where wh_id_id=%s and prod_id_id = %s", (ncnt, whid, prodid))
    else:
        inventory_lock.release()
        raise NoInventoryError(f"Invalid value for new count: {ncnt}")

    conn.commit()
    inventory_lock.release()

def view_inventory():
    #print("args:", whid, prodid, n)
    inventory_lock.acquire()
    ex_wrapper(cur,f"select wh_id_id, prod_id_id, product_quantity from {WAREHOUSE_CONTENTS};")
    #ret=get_results(cur)
    ret = cur.fetchall()
    inventory_lock.release()

    d= defaultdict(lambda : defaultdict(lambda:0))
    for row in ret:
        d[row[0]][row[1]]=row[2]

    return d


def get_matching_state_orders(state):
    rows=ex_wrapper(cur,"select ship_id, user_id_id, product_name, ups_id,"
                   "buyer_x, buyer_y, order_created_time, product_num, status"
                   f" from {ORDER_TABLE}  where status = '{state}';")
    #print("there were ", cur.rowcount , "rows matching status: ", state)

    return get_results(cur)

def get_ship_info(shipid):
    ex_wrapper(cur, "select packed_wh_id,ups_id,buyer_x, buyer_y, product_name,product_num"
                    f" from {ORDER_TABLE}  where ship_id = %s;",(shipid,))
    ret = cur.fetchall()
    assert len(ret)==1
    return ret[0]

def get_notify_info(shipid):
    ex_wrapper(cur,f"select user_id_id, product_name from "
                   f"{ORDER_TABLE} where ship_id = %s",(shipid,))
    ret=cur.fetchall()
    assert len(ret)==1
    uid ,prod_name = ret[0][0],ret[0][1]
    ex_wrapper(cur,f"select email from {AUTH_USER} where id = %s",(uid,))
    ret= cur.fetchall()
    assert len(ret)==1
    email = ret[0]
    return prod_name,email



def get_loadable_shipids(wh_id):
    ex_wrapper(cur, f"select ship_id from {ORDER_TABLE}  "
                    f"where status = 'request_noted' and packed_wh_id = %s;",
               (wh_id,))
    ret = get_results(cur)
    return [x[0] for x in ret]


def clear_db():
    ex_wrapper(cur,f"delete from {ORDER_TABLE};")
    ex_wrapper(cur,f"delete from {WAREHOUSE_CONTENTS};")
    conn.commit()

def adjust_order_status(shipid,cur_status,next_status):
    print(shipid, cur_status,next_status)
    x= ex_wrapper(cur,f"select * from {ORDER_TABLE} WHERE ship_id='{shipid}';")
    assert cur.rowcount==1

    ex_wrapper(cur,f"UPDATE {ORDER_TABLE} SET status ='{next_status}' where ship_id='{shipid}' and status ='{cur_status}';")
    conn.commit()

def set_pack_loc(shipid,wh_id):
    ex_wrapper(cur,f"UPDATE {ORDER_TABLE} SET packed_wh_id = %s where ship_id = %s;",(wh_id,shipid))
    conn.commit()

if __name__ == "__main__":
    increment_inventory(1, 2, -5)
