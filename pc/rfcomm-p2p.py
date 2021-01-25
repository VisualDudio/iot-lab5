import sys
import bluetooth
import threading

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

def start_server():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print("Waiting for connection on RFCOMM channel", port)
    client_sock, client_info = server_sock.accept()

    try:
        while True:
            raw_data = client_sock.recv(1024)
            if not raw_data:
                break
            
            data = raw_data.decode('UTF-8')
            
            print("Received car data:", data)
    except OSError:
        pass

    print("Disconnected.")

    client_sock.close()
    server_sock.close()
    print("All done.")

def start_client():
    print("Starting Client...")
    service_matches = bluetooth.find_service(uuid=uuid, address=None)

    if len(service_matches) == 0:
        print("Couldn't find the SampleServer service.")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]        

    print("Connecting to \"{}\" on {}".format(name, host))

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))

    while True:
        print("Type 'q' to quit or 'accelerate', 'brake', 'left', 'right' to control the car.")
        data = input()
        if not data:
            break
        
        sock.send(data)
        
        if data == "q":
            break
        
    sock.close()

sth = threading.Thread(target=start_server)
cth = threading.Thread(target=start_client)

sth.start()
cth.start()

cth.join()
sth.join()

print("Success, terminating")
