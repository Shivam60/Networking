try:
    import socket,sys,time,os,logging,Networking
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


class client():
    def __init__(self,host,port,path,packetsize=65536):
        self.host=host
        self.port=port
        #self.file=filenm
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
    def send(self,filenm):
        logging.info("Opening large file: ")
        nf=False
        try:
            with open(filenm,'rb') as infile:
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
        print(Networking.sz(data))
        self.sock.sendall(data)    
        et=time.time()
        
        logging.info("Sending Speed: "+str((sys.getsizeof(data)/1024**2)/(et-st))+" MBPS")
        logging.info("Closing Socket")
        self.sock.close()
    def handshake(self):
        logging.info("Connecting...")
        self.connect()
        logging.info("Sending CRC and number of files to server")
        self.sock.send((self.crc+'/\\'+str(self.file_no)+'/\\').encode('utf-8'))
        logging.info("CRC and Number of files sent.")
        logging.info("Waiting for handshake reply.")
        data=self.sock.recv(1024)
        crc,fno=Networking.find_crc_fno(data)
        logging.info("Handshake reply recieved.")
        self.sock.close()       
        if crc==self.crc and fno==self.file_no:
            logging.info("Handshake Complete")
            return True
        else:
            logging.info("Handshake Incomplete")
            logging.info("Recieved: \nCRC: "+str(crc)+"\nFile Numbers: "+str(fno))
            logging.info("Actual: \nCRC: "+str(self.crc)+"\nFile Numbers: "+str(self.file_no))
            return False
        
        
if __name__=="__main__":
    Networking.set_directory(path=r'/home/shivam/Work/Projects/test/client/')
    Networking.makedir('c_split')
    clin=client(host='localhost',port=10001,path=os.getcwd())
    a=open(os.getcwd()+'/1.mp4','rb')
    clin.stuff=a.read() 
#   clin.stuff=Networking.open(os.getcwd(),filenm='/1.mp4')
    clin.stuff=Networking.tobytes(clin.stuff)
    Networking.write(stufft=clin.stuff,name='1.bytes',dir=os.getcwd())
    clin.crc=Networking.crc_n(filenm='1.bytes')
    Networking.split(path=os.getcwd()+'/c_split/',filenm='1.bytes',chunk='3m')
    #remove to bytes function#
    clin.file_no= Networking.file_n(dir=os.getcwd()+r'/c_split/')
    if clin.handshake():
        Networking.set_directory(os.getcwd()+r'/c_split/')
        time.sleep(1)
        filelist=sorted(os.listdir())
        print(filelist)
        for file in filelist:
            clin=client(host='localhost',port=10001,path=os.getcwd())
            clin.connect()
            clin.send(filenm=file)
        Networking.set_directory(path=r'/home/shivam/Work/Projects/test/client/')
        clin.sock.close()