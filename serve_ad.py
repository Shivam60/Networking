try:
    import socket,sys,time,os,logging,subprocess
    from Networking import Network
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    '''
    try:
        logging.stream=sys.stdout
        logging.basicConfig(filemode='a',filename='log.log',level=logging.DEBUG,format='%(module)s %(levelname)s %(threadName)s %(asctime)s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())
    except ValueError as e:
        print("Cannot Create log files: Program Exiting.\nError: ")
        Logger.exception(e)
        os._exit(0)
    finally:
        print("Loggers set, imports completed")
    '''


class server(Network):
    def __init__(self,host,port,packetsize,path,filenm,lm=1):
        print("Initalizing Attributes")
        print("Checking if host and port are available: ")        
        self.host=host
        self.port=port
        self.lm=lm
        self.packetsize=packetsize
        self.recvstuff=None
        Network.__init__(self,path=path,file=filenm)
        #creating a socket with IP4 config and TCP stream protocol
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #to connect to a host and port and listen for connections
    def connect(self):
        nf=False
        try:
            print("Binding the Socket to host and Port: ")
            self.sock.bind((self.host,self.port))
        except socket.error as e:
            print("Cannot Bind the socket to Host %s and Port %d \n" %(self.host,self.port))
            print(e)
            nf=True
        finally:
            if nf:
                os._exit(0)
            print("The Server Socket is now being binded to host: %s and port: %d "%(self.host,self.port))
            #Socket listining to max 1 connection
            print("Server socket is listing for 1 connections")
            self.sock.listen(1)
    def start(self):
        self.connect()
        i=0
        self.recvstuff=b""
        stt=time.time()
        while i<self.lm:
            print("Waiting for the connection: ")
            conn,addr=self.sock.accept()
            print("Connection Recieved from connection %s and address %s"%(conn,addr))            
            recvstufftemp=b''           
            data=conn.recv(self.packetsize)
            print("Started Recieving Data: ")
            st=time.time()
            while data:                
                recvstufftemp+=data
                data=conn.recv(self.packetsize)
            et=time.time()
            #self.write(self.recvstuff,name=str(i)+'.bytes',dir=os.getcwd()+str(r'/s_split'))
            print("Speed of data transfer is "+str((sys.getsizeof(recvstufftemp)/1024**2)/(et-st))+" MBPS")
            print("Closing Socket")
            conn.close()
            self.recvstuff+=recvstufftemp            
            i+=1
        print("Average Speed of data transfer is "+str((sys.getsizeof(self.recvstuff)/1024**2)/(time.time()-stt))+" MBPS")
        print("Total Data Recieved: "+str((sys.getsizeof(self.recvstuff)/1024**2)))
        print("CRC: "+str(self.crc_n(crcstuff=self.recvstuff)))

    def handshake(self):
        print("Connecting...")
        self.connect()
        conn,addr=self.sock.accept()
        print("Connection recieved.")     
        print("Waiting for handshake reply.")  
        data=conn.recv(self.packetsize)
        print("Handshake reply recieved.")
        #print(data) 
        self.crc,self.file_no=self.find_crc_fno(data)
        print("Sending handshake back") 
        conn.send((self.crc+'/\\'+str(self.file_no)+'/\\').encode('utf-8'))
        print("Handshake back sent")
        self.sock.close()
    def makedir(self):
        print("Making Temprorary Server Directory: ")
        try:
            subprocess.run(['mkdir','s_split'])
        except subprocess.CalledProcessError as err:
            print("Cannot make directory. Program exit.\n"+str(p))
            os._exit(0)
        finally:
            print("Directory made succesfully")
if __name__=="__main__":
#    192.168.43.9
    serv=server(host='localhost',port=10001,lm=1,packetsize=65536,path=os.getcwd(),filenm='s.bytes')
    serv.handshake()
    serv.sock.close()
#    serv.makedir()
    serv=server(host='localhost',port=10001,lm=serv.file_no,packetsize=65536,path=os.getcwd(),filenm='s.bytes')
    serv.start()
