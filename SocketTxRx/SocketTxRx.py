import socket
import argparse # to get cmd line args
import time
from multiprocessing import Process

def getArguments():
    parser = argparse.ArgumentParser(description='Send and Receive multicast.')
    parser.add_argument('--rx-ip', dest='RxIp', default='', type=str, help='IP Address to receive packets')
    parser.add_argument('--tx-ip', dest='TxIp', default='', type=str, help='IP Address to send packets')
    parser.add_argument('--rx-port', dest='RxPort', default='', type=int, help='Port to receive packets')
    parser.add_argument('--tx-port', dest='TxPort', default='', type=int, help='Port to send packets')
    parser.add_argument('--script-timeout', dest='timeout', default='5', type=int, help='Script elapse time in seconds before it will exit')


def openMulticastUdpTx(TxIp, TxPort):

    # init the socket
    TransmitSock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_DGRAM) # UDP
    print("Sending packets to IP:       {}".format(TxIP))
    print("Sending packets to UDP Port: {}".format(TxPort))
    return TransmitSock

def openMulticastUdpRx(RxIp, RxPort):
    ReceiveSock = socket.socket(socket.AF_INET, # Internet
                                socket.SOCK_DGRAM) # UDP
    try:
        ReceiveSock.setsockopt(socket.SOL_SOCKET,
                                socket.SOCK_DGRAM)
    except AttributError:
        pass
    ReceiveSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    ReceiveSock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
    ReceiveSock.settimeout(10)
    ReceiveSock.bind(('', RxPort))
    host = socket.gethostbyname(socket.gethostname())
    ReceiveSock.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(host))
    ReceiveSock.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(RxIP) + socket.inet_aton(host))
    return ReceiveSock

def ReceiveMessages():

    scriptStartTime = time.time()
    args = getArguments()
    ReceiveSock = openMulticastUdpRx(args.RxIp, args.RxPort)

    while 1:
        scriptElapsedTime = time.time() - scriptStartTime
        if scriptElapsedTime > args.timeout:
            break

        data = ReceiveSock.recv(1024)


def SendMessages():

    args = getArguments()
    TransmitSock = openMulticastUdpTx(args.TxIp, args.TxPort)

    frame = "Data to send"
    TransmitSock.sendto(fram, (args.TxIp, args.TxPort))

def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()

def main():
    runInParallel(SendMessages, ReceiveMessages)


if __name__ == '__main__':
    main()


