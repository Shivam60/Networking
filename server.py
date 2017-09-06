try:
    import socket,sys,time,os,logging,subprocess,Networking
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    try:
        logging.stream=sys.stdout
        logging.basicConfig(filemode='a',filename='log.log',level=logging.DEBUG,format='%(module)s %(levelname)s %(threadName)s %(asctime)s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())
    except ValueError as e:
        logging.info("Cannot Create log files: Program Exiting.\nError: ")
        Logger.exception(e)
        os._exit(0)
    finally:
        logging.info("Loggers set, imports completed")



class server():
    def __init__(self,host,port,packetsize,path,filenm):
        logging.info("Initalizing Attributes")
        logging.info("Checking if host and port are available: ")        
        self.host=host
        self.port=port
        self.packetsize=packetsize
        self.recvstuff=None
        self.file_no=1
        #creating a socket with IP4 config and TCP stream protocol
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #to connect to a host and port and listen for connections
    def connect(self):
        nf=False
        try:
            logging.info("Binding the Socket to host and Port: ")
            self.sock.bind((self.host,self.port))
        except socket.error as e:
            logging.error("Cannot Bind the socket to Host %s and Port %d \n" %(self.host,self.port))
            logging.error(e)
            nf=True
        finally:
            if nf:
                os._exit(0)
            logging.info("The Server Socket is now being binded to host: %s and port: %d "%(self.host,self.port))
            #Socket listining to max 1 connection
            logging.info("Server socket is listing for 1 connections")
            self.sock.listen(1)
    def start(self):
        self.connect()
        i=0
        self.recvstuff=b""
        stt=time.time()
        while i<self.file_no:
            logging.info("Waiting for the connection: ")
            conn,addr=self.sock.accept()
            logging.info("Connection Recieved from connection %s and address %s"%(conn,addr))            
            recvstufftemp=b''           
            data=conn.recv(self.packetsize)
            logging.info("Started Recieving Data: ")
            st=time.time()
            while data:                
                recvstufftemp+=data
                data=conn.recv(self.packetsize)
            et=time.time()            
            logging.info("Speed of data transfer is "+str((sys.getsizeof(recvstufftemp)/1024**2)/(et-st))+" MBPS")
            logging.info("Closing Socket")
            conn.close()
            self.recvstuff+=recvstufftemp            
            i+=1
            if recvstufftemp:
                Networking.write(stufft=recvstufftemp,name=str(i)+'.bytes',dir=os.getcwd()+str(r'/s_split'))
        logging.info("Average Speed of data transfer is "+str((sys.getsizeof(self.recvstuff)/1024**2)/(time.time()-stt))+" MBPS")
        logging.info("Total Data Recieved: "+str((sys.getsizeof(self.recvstuff)/1024**2)))
        #logging.info("CRC: "+str(self.crc_n(crcstuff=self.recvstuff)))
    def handshake(self):
        logging.info("Connecting...")
        self.connect()
        conn,addr=self.sock.accept()    
        logging.info("Connection recieved.")        
        logging.info("Waiting for handshake reply.")  
        data=conn.recv(self.packetsize)
        logging.info("Handshake reply recieved.")
        #print(data) 
        self.crc,self.file_no=Networking.find_crc_fno(data)
        logging.info("Sending handshake back") 
        conn.send((self.crc+'/\\'+str(self.file_no)+'/\\').encode('utf-8'))
        logging.info("Handshake back sent")
        
        conn.close()
        self.sock.close()
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)        

if __name__=="__main__":
#    192.168.43.9
    Networking.set_directory(path=r'/home/shivam/Work/Projects/test/server/')
    Networking.makedir('s_split')
    serv=server(host='localhost',port=10001,packetsize=65536,path=os.getcwd(),filenm='s.bytes')
    serv.handshake()
    serv.start()
