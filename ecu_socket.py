import socket
import string
import secrets
import hashlib
from rsa import *

port  = 8000
host = "127.0.0.1"

def generateRandomString(length):
    charatcters = string.ascii_letters+string.digits+string.punctuation
    random_string = "".join(secrets.choice(charatcters) for _ in range(length))
    return random_string


def ecu_server():
    ecu_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ecu_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    ecu_socket.bind((host,port))

    ecu_socket.listen(5)
    print("Ecu server started and listening")

    while True:

        #accept tester connection
        tester_socket,address =  ecu_socket.accept()
        print("Reciverd connection from the tester:", address)

        # gerate random string 
        challenge_string = generateRandomString(128)
        challenge_string_hash = hashlib.sha256(challenge_string.encode('utf-8')).hexdigest()

        # sending challenge string to the tester socket
        tester_socket.sendall(challenge_string_hash.encode())
        print("Challange string is successfully sent to the tester ")

        #build connection between ecu and the Trust center
        trust_center_socket,trust_address = ecu_socket.accept()
        print("Connections established between ecu and trust center")

        # recieve public key form the truest center
        public_key =  trust_center_socket.recv(4096).decode()
        print(" public key recieved from the trust center")

        # recieve signed response from the tester
        signed_response = tester_socket.recv(4096)
        signed_response_valid = rsa_verify(signed_response,public_key,challenge_string_hash)

        if signed_response_valid:
            print("Signature is valid \n Now i can to to tester securely")
            response = "access granted!"
            tester_socket.send(response.encode())

        else:
            print("signature is invalid \n so access denied")
            response = "Access denied"
            tester_socket.send(response.encode())

if __name__ == "__main__":
    ecu_server()







