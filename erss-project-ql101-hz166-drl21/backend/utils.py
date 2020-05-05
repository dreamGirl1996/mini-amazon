import threading

def filter_world_unseen(seen_set,iterable):
    return filter(lambda x: x.seqnum not in seen_set, iterable)

def filter_ups_unseen(seen_set,iterable):
    return filter(lambda x: x.seqNum not in seen_set, iterable)

global_lock= threading.Lock()
