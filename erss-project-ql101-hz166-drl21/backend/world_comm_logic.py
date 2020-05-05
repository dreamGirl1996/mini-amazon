import db_interface
from seqnum_handler import get_seqnum
from commu_handler import read_serialized_pbuf, send_pbuf
import ups_amazon_pb2 as uapb2
import world_amazon_pb2 as wapb2
from utils import filter_world_unseen



def create_refill_request(world_comm_data,minimum=500):
    inv=db_interface.view_inventory()
    for wh_id in db_interface.get_whids():
        seqnum = get_seqnum()
        purchase_pb = wapb2.APurchaseMore()
        purchase_pb.whnum = wh_id
        purchase_pb.seqnum = seqnum
        for prodid in db_interface.get_prodids():
            if inv[wh_id][prodid]<minimum:
                print("refill needed")
                prod_pb = wapb2.AProduct()
                prod_pb.id, prod_pb.description, prod_pb.count = prodid, 'UNUSED FIELD', minimum
                purchase_pb.things.append(prod_pb)
                world_comm_data.track_new_message(seqnum,'APurchaseMore',purchase_pb)


def world_response_handler(serialized_msg, world_comm_data,ups_comm_data):
    world_response_pb = wapb2.AResponses()
    world_response_pb.ParseFromString(serialized_msg)
    print("world response:-------",world_response_pb)
    print("----------------------------")
    if world_response_pb.error:
        for x in world_response_pb.error:
            print(x.err, world_comm_data._all_messages[x.originseqnum])
        raise AssertionError("world returned error")


    for a_seqnum in world_response_pb.acks:
        world_comm_data.handle_acked_message(a_seqnum)

    seen_seqnums = world_comm_data.all_seen_seqnums
    should_ack = set()
    for purchase_pb in filter_world_unseen(seen_seqnums,world_response_pb.arrived):
        for mul_prod in purchase_pb.things:
            db_interface.increment_inventory(purchase_pb.whnum, mul_prod.id, mul_prod.count)
        world_comm_data.register_incoming_seqnum(purchase_pb.seqnum)

    pickup_requests = {}
    for wh_id in db_interface.get_whids():
        seqnum = get_seqnum()
        pickup_req_pb = uapb2.AtoUPickupRequest()
        pickup_req_pb.seqNum = seqnum
        pickup_req_pb.warehouseId=wh_id
        pickup_requests[wh_id]=pickup_req_pb

    for packed_pb in filter_world_unseen(seen_seqnums,world_response_pb.ready):
        #db_lock.acquire() locking unecessary
        shipid=packed_pb.shipid
        shipinfo = uapb2.ShipInfo()
        wh_id, ups_acc, dest_x, \
        dest_y, prod_name, prod_num = db_interface.get_ship_info(shipid)
        shipinfo.shipId=shipid
        shipinfo.destination_x=dest_x
        shipinfo.destination_y=dest_y
        if ups_acc:
            shipinfo.UPSaccount=ups_acc
        product = uapb2.Product()
        product.description=prod_name
        product.count= prod_num
        shipinfo.products.append(product)
        pickup_requests[wh_id].shipment.append(shipinfo)
        #TODO: change this to accomodate ack in the future- here i assume requests are noted
        db_interface.adjust_order_status(packed_pb.shipid,"to pack","request_pickup")
        world_comm_data.register_incoming_seqnum(packed_pb.seqnum)
    for wh_id in pickup_requests:
        req = pickup_requests[wh_id]
        if req.shipment:
            ups_comm_data.track_new_message(req.seqNum,'AtoUPickupRequest',req)

    for loaded_pb in filter_world_unseen(seen_seqnums,world_response_pb.loaded):
        db_interface.adjust_order_status(loaded_pb.shipid,"load","loaded")
        shipid=loaded_pb.shipid
        ups_comm_data.track_loaded_package(shipid)
        world_comm_data.register_incoming_seqnum(loaded_pb.seqnum)




def send_world_requests(world_sock,world_comm_data):
    pb_dict = world_comm_data.unacked_protobuf_dict
    command_pb = wapb2.ACommands()
    command_pb.buy.extend(pb_dict['APurchaseMore'].values())
    command_pb.topack.extend(pb_dict['APack'].values())
    command_pb.load.extend(pb_dict['APutOnTruck'].values())
    command_pb.queries.extend(pb_dict['AQuery'].values())
    command_pb.acks.extend(world_comm_data.pop_all_acks())
    print("sending to world:-------------------",command_pb)
    print("------")
    send_pbuf(world_sock,command_pb)



def make_pack_requests(world_comm_data):
    pending = db_interface.get_matching_state_orders('pending')
    for o in pending:
        ship_id=o[0]
        x,y=o[4],o[5]
        prodname=o[2]
        count = o[7]
        whid = db_interface.get_matching_wh(x,y)
        prodid = db_interface.get_matching_prodid(prodname)

        prod_desc = db_interface.get_prod_desc(prodid)
        prod_pb = wapb2.AProduct()
        prod_pb.id = prodid
        prod_pb.description = prod_desc
        prod_pb.count = count
        try:
            db_interface.increment_inventory(whid, prodid, -count)
        except db_interface.NoInventoryError:
            continue

        db_interface.adjust_order_status(ship_id, 'pending', 'to pack')
        db_interface.set_pack_loc(ship_id,whid)
        pack_pb = wapb2.APack()
        pack_pb.whnum = whid
        pack_pb.shipid = ship_id
        seqnum = get_seqnum()
        pack_pb.seqnum = seqnum
        world_comm_data.track_new_message(seqnum,'APack',pack_pb)



