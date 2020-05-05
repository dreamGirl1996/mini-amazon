import threading
lock = threading.Lock()
private_seqnum = 0

def get_seqnum():
    global private_seqnum
    lock.acquire()
    private_seqnum+=1
    out = private_seqnum
    lock.release()
    return out

