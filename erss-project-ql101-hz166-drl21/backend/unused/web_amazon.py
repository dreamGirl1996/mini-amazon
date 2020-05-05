from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
import socket


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

def web_request(client_sock):
    try:
        web_request_str = read_varint_delimited_stream(client_fd)
        web_request = web_amazon_pb2.WACommand()
        web_request.ParseFromString(web_request_str)
        print("-------request from web-------\n", str(web_request), "\n--------end request---------")

        for neworder in web_request.place:
            product_list = query_product(neworder.order_id)  # list of product to buy (type: AProduct())
            # maybe not exist
            if neworder.instock:
                # product in database has already been reduced
                send_pack_to_world(neworder.order_id, neworder.whnum, product_list)
            else:
                send_purchase_more_to_world(neworder.order_id, neworder.whnum, product_list)
        for newchange in web_request.change:  # newchange.order_id , dest_x, dest_y
            aucommand = amazon_ups_pb2.AUCommands()
            aucommand.change_destination.package_id = newchange.order_id
            aucommand.change_destination.new_destination_x = newchange.dest_x
            aucommand.change_destination.new_destination_y = newchange.dest_y
            send_request_on_socket(aucommand, ups_sock)
    except Exception as ex:
        print(str(ex))