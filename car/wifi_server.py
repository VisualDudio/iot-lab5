import socket
from car import Car

HOST = "192.168.1.184"
PORT = 8080

car = Car()

def process_request(request):
    response = "OK"
    
    if request == "GET":
        print(car)
        response = car.get_data()
    else:
        print(request)
        command = request.split(' ')[1]
        response = car.process_command(command)
    
    return response

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            print("server recv from: ", clientInfo)
            raw_request = client.recv(1024)
            if not raw_request:
                continue
            
            request = raw_request.decode('UTF-8')
            response = process_request(request)
            
            client.sendall(response.encode('UTF-8'))
    except Exception as e: 
        print(e)
        print("Closing socket")
        client.close()
        s.close()
