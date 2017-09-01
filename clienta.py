try:
    import socket,sys,time,os,logging
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    pass
'''
    try:
        logging.stream=sys.stdout
        logging.basicConfig(filename='log'+time.strftime("%m%d%s")+'.log',level=logging.DEBUG,format='%(module)s %(levelname)s %(threadName)s %(asctime)s %(message)s')
        logging.getLogger().addHandler(logging.StreamHandler())
    except ValueError as e:
        logging.info("Cannot Create log files: Program Exiting.\nError: ")
        Logger.exception(e)
        os._exit(0)
    finally:
        logging.info("Loggers set, imports completed")  
'''
def gen(file,sz):
    with open(file,'wb') as outfile:
        outfile.seek(sz-1)
        outfile.write(b'\0')
        outfile.close()
#from sendfile import sendfile
class client():
    def __init__(self,host,port,file):
        self.host=host
        self.port=port
        self.file=file
        self.sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def connect(self):
        nf=False
        try:
            print("connecting the Socket to server on port: ")
            self.sock.connect((self.host,self.port))
        except socket.error as e:
            logging.error("Cannot connect the socket to server %s on Port %s: \n" %(self.host,self.port))
            logging.error(e)
            nf=True
        finally:
            if nf:
                os._exit(0)
            print("The Client Socket has been connected to server: %s on port: %d "%(self.host,self.port))
        print("Opening large file: ")
    def send(self):
        nf=False
        try:
            with open(self.file,'rb') as infile:
                data=infile.read()
        except IOError as e:
            logging.error("Error has occurerd with the file: ")
            logging.error(e)
        finally:
            infile.close()
            if nf:
                os_exit(0)
            print("File copied into memory: ")
            
        print("Sending large file: ")
        st=time.time()
        self.sock.sendall(data)
        et=time.time()
        print("Sending Speed: "+str((sys.getsizeof(data)/1024**2)/(et-st))+" MBPS")
        print("Closing Socket")
        self.sock.close()
if __name__=="__main__":
    #gen("asv.bytes",1024*1024*1024)
    clin=client(host='192.168.43.9',port=10001,file="2.bytes")
    clin.connect()
    clin.send()
