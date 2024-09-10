import socket


def tester():
    try:
        ecu_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ecu_socket.connect(())
    except:
        print("ecu server is down")
     
    # recieve challenge string from ecu
    challenge_string =  ecu_socket.recv(1024).decode()
    if challenge_string == "":
        print("Access denied!")
        return
    
    # connect to trust center
    trust_center_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    trust_center_socket.connect(())

    # send the challenge string which is recieved from the ecu - socket
    trust_center_socket.send(challenge_string.encode())
    print("Successsully sent challenge string to trust center ")

    # recieve singed resonse from the trust center and send to ecu socket
    signed_response = trust_center_socket.recv(4096)
    ecu_socket.send(signed_response)
    print("Successfully sent signed response from trust center to ECU socket")

    # recieve the response from the Ecu socket
    access_status =  ecu_socket.recv(1024).decode()

    print("Access Status recieved from the ECU :" ,access_status)

if __name__ == "__main__":
    tester()
