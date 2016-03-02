from enigmaMachine import *
import socket, sys
"""
This file works as the runner for the enigmaMachine class
Allows for sending / receiving encrypted messages
When excuting this the first argument must be a config file location for the configuartion of the machine



"""
"""
Specifications for config file:
    1) The first line specifies whether it is the client or server
        do this by wither writing out 'client' or 'server' on this line
    2) The second line specifies the host

"""
def client_mode(machine, server):
    print("Acting as client")
    serverName= server
    #serverName = 'localhost'
    serverPort = 12000
    clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    clientSocket.connect((serverName,serverPort))
    while True:
        try:
            sendMsg=input("What is your message? ")
            byteMsg = (machine.encrypt(sendMsg)).encode()
            clientSocket.send(byteMsg)
            byteRecv= clientSocket.recv(1024) # no more than 1024 bytes
            print("message received")
            print(machine.decrypt(byteRecv.decode()))
        except IOError:
            print("message receive failed, closing connection")
            clientSocket.close()
            break

def server_mode(machine):
    print("Acting as server")
    serverPort = 12000
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    #Prepare a sever socket
    serverSocket.listen(1)
    print('Waiting ...')
    connectionSocket, addr = serverSocket.accept()
    while True:

        try:
            message = connectionSocket.recv(1024)
            byteRecievedMessage = message.decode()
            print(machine.decrypt(byteRecievedMessage))
            sendMsg = input("What is your message? ")
            byteSendMessage = (machine.encrypt(sendMsg)).encode()
            connectionSocket.send(byteSendMessage)
            print("message sent")

        except IOError:
            print("message receive failed, closing connection")
            connectionSocket.close()
            break

    connectionSocket.close()
    serverSocket.close()

def main():
    machine = enigmaMachine()
    clientMode = True
    fileName = sys.argv[1]
    file = open(fileName, 'r')
    f = file.read().split("\n")
    host = f[1]
    if f[0] == "server":
        clientMode = False
    del f[0]
    del f[0]
    for line in f:
        info = line.split(", ")
        machine.addTumbler(info[0], info[1].split(" "), info[2])

    if clientMode:
        client_mode(machine, host)
    else:
        server_mode(machine)

if __name__ == "__main__":
    main()