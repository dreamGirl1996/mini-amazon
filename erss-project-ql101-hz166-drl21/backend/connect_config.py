import socket
name = socket.gethostname()
print(name)
if "dan-laptop" in name:
    print("dan's laptop")
    dan = True
else:
    print('Using ql101"s connect settings')
    dan=False

ups_listen_port = 6666
world_a_port = 23456
world_u_port = 12345
web_listen_port = 6888
db_port = 5433
if "dan-laptop" in name:
    amazon_addr, ups_addr, world_addr= 'localhost', 'localhost', 'localhost'
    db_host = 'localhost'
elif "8302" in name:
    amazon_addr= 'vcm-8302.vm.duke.edu'
    ups_addr = 'vcm-8302.vm.duke.edu'
    world_addr = 'vcm-8302.vm.duke.edu'
    db_host = 'vcm-8302.vm.duke.edu'
elif "14733" in name:
    print('ups machine')
    db_host = 'localhost'
    db_port = 5432
    ups_addr = 'localhost'
    world_addr = 'localhost'
    amazon_addr = 'localhost'
elif "14692" in name:
    print('ups machine 2')
    db_host = 'localhost'
    db_port = 5432
    ups_addr = 'localhost'
    world_addr = 'localhost'
    amazon_addr = 'localhost'
else:
    print('unknown host')
    exit(1)
