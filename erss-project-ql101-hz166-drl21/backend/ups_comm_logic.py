import db_interface
from seqnum_handler import get_seqnum
import ups_amazon_pb2 as uapb2
import world_amazon_pb2 as wapb2
from commu_handler import send_pbuf
import threading
import utils
import mail_notifier
truckload_lock = threading.Lock()


def ups_response_handler(serialized_msg, ups_comm_data, world_comm_data):
    ups_response_pb = uapb2.UtoACommand()
    ups_response_pb.ParseFromString(serialized_msg)
    print("ups response ----")
    print(ups_response_pb)
    print("------")

    # print(world_response_pb)
    if ups_response_pb.errMsg:
        print(ups_response_pb.errMsg)
        raise AssertionError("I don't know how to handle errors")
    awaiting_confirm = ups_comm_data.await_pickup_confirm_dict
    for a_seqnum in ups_response_pb.ack:
        ups_comm_data.handle_acked_message(a_seqnum)

    seen_set = ups_comm_data.all_seen_seqnums

    for msg in utils.filter_ups_unseen(seen_set,ups_response_pb.usrVlid):
        ups_comm_data.register_incoming_seqnum(msg.seqNum)
        success=msg.result
        id = msg.shipId
        if success:
            db_interface.adjust_order_status(id,'val_req_sent','pending')
        else:
            db_interface.adjust_order_status(id,'val_req_sent','invalid')

    truckload_lock.acquire()
    for idx, msg in enumerate(utils.filter_ups_unseen(seen_set, ups_response_pb.loadReq)):
        #print(f"loadreq{idx}:",msg)
        wh_id = msg.warehouseId
        truckid = msg.truckId
        not_loaded = ups_comm_data.truck_notloaded
        expecting = ups_comm_data.truck_expecting
        try:
            #pass #because they send multiple
            assert truckid not in not_loaded and truckid not in expecting
        except Exception as e:
            import pdb;pdb.set_trace()
            raise e
        for shipid in msg.shipId:
            snum = get_seqnum()
            put_on_truck_pb = wapb2.APutOnTruck()
            put_on_truck_pb.whnum = wh_id
            put_on_truck_pb.truckid = msg.truckId
            put_on_truck_pb.seqnum = snum
            put_on_truck_pb.shipid = shipid
            world_comm_data.track_new_message(snum, 'APutOnTruck', put_on_truck_pb)
            db_interface.adjust_order_status(shipid, 'request_pickup', 'load')
            ups_comm_data.track_loading_package(shipid, msg.truckId)
        ups_comm_data.register_incoming_seqnum(msg.seqNum)
    truckload_lock.release()

    for msg in utils.filter_ups_unseen(seen_set, ups_response_pb.delivery):
        db_interface.adjust_order_status(msg.shipId, 'delivering', 'delivered')
        name,email = db_interface.get_notify_info(msg.shipId)
        mail_notifier.notify_arrival(name,email)
        ups_comm_data.register_incoming_seqnum(msg.seqNum)


def send_ups_requests(ups_sock, ups_comm_data):
    pb_dict = ups_comm_data.unacked_protobuf_dict
    command_pb = uapb2.AtoUCommand()
    command_pb.usrVlid.extend(pb_dict['UserValidationRequest'].values())
    command_pb.pikReq.extend(pb_dict['AtoUPickupRequest'].values())
    command_pb.loadReq.extend(pb_dict['AtoULoadFinishRequest'].values())
    command_pb.errMsg.extend(pb_dict['ErrorMessage'].values())
    command_pb.ack.extend(ups_comm_data.pop_all_acks())
    print("sending ups ----")
    print(command_pb)
    print("------")
    send_pbuf(ups_sock, command_pb)


def create_loadfinish_requests(ups_comm_data):
    truckload_lock.acquire()
    expecting = ups_comm_data.truck_expecting

    ready_ids = ups_comm_data.ready_truckids()
    for truckid in ready_ids:
        finish_pb = uapb2.AtoULoadFinishRequest()
        snum = get_seqnum()
        finish_pb.seqNum = snum
        finish_pb.truckId = truckid
        finish_pb.shipId.extend(expecting[truckid])
        print("finished loading for truck: ", truckid, "shipids:",
              expecting[truckid])
        for shipid in expecting[truckid]:
            db_interface.adjust_order_status(shipid,'loaded','delivering')
        ups_comm_data.clear_truck_data(truckid)
        ups_comm_data.track_new_message(snum, 'AtoULoadFinishRequest', finish_pb)

    truckload_lock.release()

def create_val_requests(ups_comm_data):
    need_valids=db_interface.get_matching_state_orders('await_valid')
    for row in need_valids:
        valid_pb=uapb2.UserValidationRequest()
        seqnum = get_seqnum()
        valid_pb.seqNum = seqnum
        valid_pb.UPSaccount = row[3]
        valid_pb.shipId=row[0]
        ups_comm_data.track_new_message(seqnum,'UserValidationRequest',valid_pb)
        db_interface.adjust_order_status(row[0],'await_valid','val_req_sent')
