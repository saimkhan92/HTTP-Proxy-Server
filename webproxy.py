import socket
import thread
import hashlib
from datetime import datetime
import sys

def main():
    while True:
        
        server_port=12341
        sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(("127.0.0.1", server_port))
        except:
            print("PORT ALREADY IN USE. (also check that you entered a valid IP if you get multiple errors)")
            raise SystemExit
        
        sock.listen(2)
        print("socket is now listening from browser\n")
        clientSocket,clientAddress= sock.accept()
        thread.start_new_thread(internet_func,(clientSocket,clientAddress))
        print('Creating new thread for the internet')
    sock.close()
    print("main socket closed")



def internet_func(clientSocket,clientAddress):  
    
    cache_flag="not found"
    cached_data=""     
    print("Connection from {}".format(clientAddress))
    browser_data= clientSocket.recv(409600)
    
    if len(browser_data)>0:
        browser_data_list=browser_data.split()
        #print("RECEIVED : \n "+str(browser_data))
        print("RECEIVED LIST : "+str(browser_data_list))
        hash_object=hashlib.md5(browser_data_list[1])
        hash_key=hash_object.hexdigest()
        
        
        if len(cache_dict)>0:  
            for key in cache_dict:
                if key==hash_key:
                    time_b=datetime.now()
                    difference=(time_b-time_stamp[hash_key]).total_seconds()        # checking for cache timeout 
                    if difference<timeout_input:
                        print("previous cache entry found")
                        print(key)
                        print(hash_key)
                        clientSocket.sendall(cache_dict[key])
                        cache_flag="found"
                    else:
                        print("\ncache timeout expired, cache will not be processed")
                    
        if browser_data_list[0]=="GET" and browser_data_list[2]=="HTTP/1.0":                 #checking if the request s a GET request
            if cache_flag=="not found":
                print("GET found")
                print("key of the dictionary:")
                print(browser_data_list[1])
                print("")
                hostnew = browser_data_list[4]
                print("Host name: ", hostnew)
                print(hostnew)
        
                sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock2.connect((hostnew, 80))
                sock2.sendall(browser_data)
                print ('data sent by proxy thread back to the browser')
                while True:
                    sock2.settimeout(2.0)
    
                    try:  
                        print("receiving from internet 1 \n")
                        internet_data=sock2.recv(4096)
                        if not len(internet_data)>0:
                            cache_dict[hash_key]=cached_data
                            time_stamp[hash_key]=datetime.now()
                            print("cache entry created IF NOT")
                            print(len(cache_dict))
                            break 
                        print("receiving from internet 2\n")
                        print(internet_data)
                        cached_data=cached_data+internet_data               # storing data in the cache   
                        
                    except:
                        cache_dict[hash_key]=cached_data
                        time_stamp[hash_key]=datetime.now()
                        print("cache entry created EXCEPT")
                        print(len(cache_dict))
                        break
                    
                    clientSocket.sendall(internet_data)                     # sending data back to the client
                
                sock2.close()
                print("sock2 closed")
            clientSocket.close()
            print("clientsocket closed\n")


    
if __name__=="__main__":
    cache_dict={}
    time_stamp={}
    time_a=""
    time_b=""
    difference=""

    if len(sys.argv)!=2:
        print("Error! Please enter the value of cache timeout in seconds as an argument")
        raise SystemExit
        
    timeout_input=int(sys.argv[1])
    main()


        
    



