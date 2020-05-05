from collections import defaultdict
from threading import Lock
class Comm_Data:
    def __init__(self):
        self.unacked_protobuf_dict = defaultdict(dict)#pb_type:seq_num:protobuf
        self._seqnum_to_pbtype_dict= {}
        self.seqnum_pbtype_dict = {}
        self.received_shouldack=set()#numbers
        self.received_ack_lock=Lock()
        self.seen_seqnum_lock = Lock()
        self.all_seen_seqnums = set()

        self._all_messages= {}


    def extend_shouldack(self,vals):
        self.received_ack_lock.acquire()
        self.received_shouldack=self.received_shouldack.union(vals)
        self.received_ack_lock.release()

    def pop_all_acks(self):
        self.received_ack_lock.acquire()
        ret= self.received_shouldack
        self.received_shouldack=set()
        self.received_ack_lock.release()
        return ret

    def track_new_message(self,seqnum,pb_type,pb):
        self._seqnum_to_pbtype_dict[seqnum]=pb_type
        self.unacked_protobuf_dict[pb_type][seqnum]=pb
        self._all_messages[seqnum]=pb

    def handle_acked_message(self,seqnum):
        if seqnum not in self._seqnum_to_pbtype_dict:
            for d in self.unacked_protobuf_dict.values():
                assert seqnum not in d
            return
            #duplicate acks possible. Assume this was one...

        assert seqnum in self._seqnum_to_pbtype_dict
        type =  self._seqnum_to_pbtype_dict[seqnum]
        del self._seqnum_to_pbtype_dict[seqnum]
        assert seqnum in self.unacked_protobuf_dict[type]
        del self.unacked_protobuf_dict[type][seqnum]

    def register_incoming_seqnum(self,seqnum):
        self.seen_seqnum_lock.acquire()
        if seqnum not in self.all_seen_seqnums:
            self.received_shouldack.add(seqnum)
        self.all_seen_seqnums.add(seqnum)
        self.seen_seqnum_lock.release()

class UPS_Comm_Data(Comm_Data):
    def __init__(self):
        super().__init__()
        self.disconnect=False
        self.truck_expecting = defaultdict(set)
        self.truck_notloaded=defaultdict(set)
        self.shipid_to_truckid={}
        self.await_pickup_confirm_dict={}

    def track_loading_package(self,shipid,truckid):
        self.truck_expecting[truckid].add(shipid)
        self.truck_notloaded[truckid].add(shipid)
        self.shipid_to_truckid[shipid]=truckid

    def track_loaded_package(self,shipid):
        truckid = self.shipid_to_truckid[shipid]
        self.truck_notloaded[truckid].remove(shipid)

    def ready_truckids(self):
        out= []
        for id in self.truck_expecting:
            if self.truck_ready(id):
                out.append(id)

        return out

    def truck_ready(self,truckid):
        assert truckid in self.truck_expecting
        if not self.truck_notloaded[truckid]:
            return True
        return False

    def clear_truck_data(self,truckid):
        assert truckid in self.truck_expecting and truckid in self.truck_notloaded
        assert not self.truck_notloaded[truckid]
        del self.truck_expecting[truckid]
        del self.truck_notloaded[truckid]

        to_remove = set()
        for id in self.shipid_to_truckid:
            if self.shipid_to_truckid[id] == truckid:
                to_remove.add(id)

        for id in to_remove:
            del self.shipid_to_truckid[id]