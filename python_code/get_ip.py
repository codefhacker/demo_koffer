import socket



def get_ip_adress():
    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    if IPAddr != "127.0.1.1":
        print("error reading ip adress........")
        
    return IPAddr




if __name__ == "__main__":
    print(get_ip_adress())
    


