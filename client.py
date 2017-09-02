try:
    import socket,sys,time,os,logging
  #  from sendfile import sendfile
    from Networking import Network
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    try:
        logging.stream=sys.stdout
        logging.basicConfig(filemode='w',filename='log'+'.log',level=logging.DEBUG,format='%(module)s %(levelname)s %(threadName)s %(asctime)s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())
    except ValueError as e:
        logging.info("Cannot Create log files: Program Exiting.\nError: ")
        Logger.exception(e)
        os._exit(0)
    finally:
        logging.info("Loggers set, imports completed")


class client(Network):
    def __init__(self,host,port,filenm,path,packetsize=65536):
        Network.__init__(self,path=path,file=filenm)
        self.host=host
        self.port=port
#        self.file=filenm
        self.packetsize=packetsize
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        nf=False
        try:
            logging.info("connecting the Socket to server on port: ")
            self.sock.connect((self.host,self.port))
        except socket.error as e:
            logging.error("Cannot connect the socket to server %s on Port %s: \n" %(self.host,self.port))
            logging.error(e)
            nf=True
        finally:
            if nf:
                os._exit(0)
            logging.info("The Client Socket has been connected to server: %s on port: %d "%(self.host,self.port))
    def connect_server(self):
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
    def send(self):
        logging.info("Opening large file: ")
        nf=False
        try:
            with open(self.file,'rb') as infile:
                pass
                data=infile.read()
        except IOError as e:
            logging.error("Error has occurerd with the file: ")
            logging.error(e)
        finally:
            infile.close()
            if nf:
                os_exit(0)
            logging.info("File copied into memory: ")
            
        logging.info("Sending large file: ")
        st=time.time()
        offset=0
        '''
        infile=open(self.file,'rb')
        while True:
            sent=sendfile(self.sock.fileno(),infile.fileno(),offset,os.path.getsize(self.file))
            if sent==0:
                break
            offset+=sent
        '''
        self.sock.sendall(data)
        et=time.time()
        logging.info("Sending Speed: "+str((sys.getsizeof(data)/1024**2)/(et-st))+" MBPS")
        logging.info("Closing Socket")
        self.sock.close()
    def handshake(self,crc,file_no):
        #split
        #crc
        #file_no
        self.connect()
        logging.info("Sending CRC and number of files to server")
        self.sock.send((crc+'/\\'+str(file_no)+'/\\').encode('utf-8'))
        logging.info("CRC and Number of files sent.")
        data=self.sock.recv(1024)
        while not data:
            data=self.sock.recv(1024)
        print(data)        
        self.sock.close()
        
if __name__=="__main__":
    #gen("asv.bytes",1024*1024*1024)
    clin=client(host='localhost',port=10001,filenm='2.bytes',path=os.getcwd())
    #clin.handshake(crc='123',file_no=123)
    '''
    os.chdir(os.getcwd()+r'/split')
    for file in os.listdir():        
        clin=client(host='192.168.43.1',port=10001,file=file)
        clin.connect_client()
        clin.send()
    '''