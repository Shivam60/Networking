try:
    import socket,sys,time,os,logging,subprocess,Networking,pickle
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
def fromdisk(path,filenm): 
    nf=True
    t=os.getcwd()
    os.chdir(path)
    try:
        logging.info("Changing Directory")
        logging.info("Opening File")        
        infile= open(filenm,'rb')
        logging.info("Reading File")
        stuff=infile.read()
    except:
        nf=False
        logging.info("Cannot Open: ")
        #logging.exception(e)
    finally:
        if nf:
            logging.info("File read with the size of: "+str(sz(stuff))+" MB")
            infile.close()
            logging.info("Closing File")
            logging.info("Changing Directory")
            os.chdir(t)
            return stuff
#returns serialized item passed in as a parameter
def tobytes(stuff):
    nf =True
    try:
        pstuff=pickle.dumps(stuff)
    except pickle.PicklingError as e:
        nf=False
        logging.info("Error in Serialisation of the Object. Object could not be converted to byetes. Make Sure the Datatype supports serialization.")
        logging.exception(e)
    finally:
        logging.info("Cpickle has Serialized: "+str(sz(stuff))+ " MB")
        if nf:
            return pstuff
#returns deserialized item passed in as a parameter
def frombytes(pstuff):
    nf=True 
    try:
        logging.info("Serializing stuff")
        stuff=pickle.loads(pstuff)
    except pickle.UnpicklingError as e:
        nf=False
        logging.info("Error in Deserialisation of the Object. Object could not be converted to bytes.\nMake Sure the Datatype supports serialization.\n")
        logging.exception(e)
    finally:
        logging.info("Cpickle has DeSerialized: "+str(sz(pstuff))+ " MB")
        if nf:
            return stuff
    #return the compressed version of the data
def compress(self):
    nf=True
    try:
        logging.info("Compressing Stuff")
        self.stuff=gzip.compress(self.stuff)
    except:
        logging.exception("Compression Failed")
        nf=False
    finally:
        if nf:
            logging.info("Compressed Size is: "+str(self.sz())+" MB")
#return the size of the data to send in MB unit and as type float
def sz(stuff):
    logging.info("Calculating Size of Stuff")
    return sys.getsizeof(stuff)/1024**2
    #return the uncompressed version of the data
    def decompress(self):
    	nf=True
    	try:
    		logging.info("Decompressing Stuff")
    		self.stuff=gzip.compress(self.stuff)
    	except:
    		nf=False
    		logging.exception("Compression Failed: ")
    	finally:
    		if nf:
    			logging.info("Deompressed Size is: "+str(self.sz())+"MB")

#write file to disk with a supplied name
def todisk(stufft,name,dir):
    t=os.getcwd()
    os.chdir(dir)
    nf=True
    logging.info("Attempt to write file")
    try:
        with open(name,'wb') as outfile:
            outfile.write(stufft)
    except IOError as e:
        nf=False
        logging.error("Cannot write file to disk.")
        logging.exception(e)
    finally:
        if nf:
            logging.info("File written :")
            os.chdir(t)
        outfile.close()
#to Split the file into small chunks
def split(path,filenm,chunk='3M'):
    try:
        logging.info("Spliting the Files into %s parts: " %chunk)
        p=subprocess.run(['split','-b',chunk,filenm,path])
        logging.info("Changing Directory: ")
        t=os.getcwd()
        os.chdir(path)
        d={}
        logging.info("Finding CRC for each splited file: ")        
        for file in os.listdir():
            p=subprocess.run(['md5sum',file],stdout=subprocess.PIPE)
            d[str(p.stdout.decode('utf-8').split()[0])]=str(file)
    except subprocess.CalledProcessError as err:
        logging.error("Cannot Split the file. Program Exit.\n"+str(p))
        os._exit(0)
    finally:
        logging.info("Files split Succesfully")
        logging.info("Chksum being written")
        d=tobytes(stuff=d)
        print(type(d))
        todisk(stufft=d,name='CRC.bytes',dir=os.getcwd())
        logging.info("Chksum being written")
        os.chdir(t)
        logging.info("Changing Directory: ")
#to calculate the number of files splited
def file_n(dir):
    nf=True
    t=os.getcwd()
    try:
        logging.info("Entering Directory to count number of files ")
        os.chdir(dir)            
    except:
        nf=False
        logging.error('Cannot enter into Directory.')
    finally:
        if nf:
            ans=len(os.listdir())
            logging.info("Files calulcated.\nExit Directory to count number of files ")
            os.chdir(t)
            return ans
#to calculate the Check sum of the file(not working)
def crc_n(filenm):
    nf=True
    try:
        logging.info("Attempting to Find Check Sum of stuff: ")
        p=subprocess.check_output(['cksum',filenm])
    except subprocess.CalledProcessError as err:
        nf=False
        logging.error('Error at finding Check Sum of file. \n'+err)
    finally:
        if not nf:
            return
        logging.info("Check Sum Found")
        op=p.decode('utf-8').split(' ')
        op=op[0]+' '+op[1]
        return ''.join(op)
#to find crc and file number from handhsake
def find_crc_fno(data):
    logging.info('Decoding data for CRC and File Numbers')
    data=data.decode('utf-8').split('/\\')
    crc_list=data[2]
    passwo=data[3]
    file_no=int(data[1])
    crc=data[0]
    logging.info('Data decoded for CRC and File Numbers')
    return crc,file_no,crc_list,passwo

#to set the current working directory
def set_directory(path):
    try:
        logging.info("Changing the Directory: ")
        os.chdir(path)
        logging.info("Directory Changed: ")
    except:
        logging.error("Could Not Change Directory: ")
#to make a directory given by the name dir in current working directory
def makedir(dir):
    logging.info("Making Temprorary %s Directory: "%dir)
    try:
        subprocess.run(['mkdir',dir])
    except subprocess.CalledProcessError as err:
        logging.error("Cannot make directory. Program exit.\n"+str(p))
        os._exit(0)
    finally:
        logging.info("Directory made succesfully")
def join(path):
    os.chdir(path)
    try:
        logging.info("Joining the Files ")
        p=subprocess.run(['cat','x*','recv_data'])
    except subprocess.CalledProcessError as err:
        logging.error("Cannot Join the file. Program Exit.\n"+str(p))
        os._exit(0)
    finally:
        logging.info("Files Joined Succesfully")    

def join(path):
    t=os.getcwd()
    os.chdir(path)
    try:
        logging.info("Joining the Files ")
        main=b''
        for file in sorted(os.listdir()):
            f=open(file,'rb')
            main+=f.read()
            f.close()
    except :
        logging.error("Cannot Join the file. Program Exit.\n"+str(p))
        os._exit(0)
    finally:
        logging.info("Files Joined Succesfully")
        os.chdir(t) 
        f=open('downloaded.bytes','wb')
        f.write(main)
        f.close()
class server():
    def __init__(self,host,port,packetsize,path,filenm):
        logging.info("Initalizing Attributes")
        logging.info("Checking if host and port are available: ")        
        self.host=host
        self.port=port
        self.packetsize=packetsize
        self.recvstuff=None
        self.file_no=1
        self.crc_list=None
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
                todisk(stufft=recvstufftemp,name=str(i)+'.bytes',dir=os.getcwd()+str(r'/s_split'))
        logging.info("Average Speed of data transfer is "+str((sys.getsizeof(self.recvstuff)/1024**2)/(time.time()-stt))+" MBPS")
        logging.info("Total Data Recieved: "+str((sys.getsizeof(self.recvstuff)/1024**2)))
    def handshake(self):
        logging.info("Connecting...")
        self.connect()
        conn,addr=self.sock.accept()    
        logging.info("Connection recieved.")        
        logging.info("Waiting for handshake reply.")  
        data=conn.recv(self.packetsize)
        print(data)
        logging.info("Handshake reply recieved.")
        self.crc,self.file_no,self.crc_list,passw=find_crc_fno(data=data)
        logging.info("Sending handshake back") 
        conn.send((self.crc+'/\\'+str(self.file_no)+'/\\'+self.crc_list+'/\\'+passw).encode('utf-8'))
        logging.info("Handshake back sent")
if __name__=="__main__":
#    192.168.43.9
    set_directory(path=r'/home/shivam/Work/Projects/test/server/')
    makedir('s_split')
    serv=server(host='localhost',port=10001,packetsize=65536,path=os.getcwd(),filenm='s.bytes')
    serv.handshake()
    serv.start()
    set_directory(path=r'/home/shivam/Work/Projects/test/server/s_split')
    d={}
    logging.info('Finding CRC file.')
    for file in os.listdir():
        p=subprocess.run(['cksum',file],stdout=subprocess.PIPE)
        d[str(p.stdout.decode('utf-8').split()[0])+' '+str(p.stdout.decode('utf-8').split()[1])]=str(file)
    logging.info('Finding contents from CRC file.')
    crc_bytes=frombytes(pstuff=fromdisk(filenm=str(d[serv.crc_list]),path=os.getcwd()))
    d={}
    for file in os.listdir():
        p=subprocess.run(['md5sum',file],stdout=subprocess.PIPE)
        d[str(p.stdout.decode('utf-8').split()[0])]=str(file)
    logging.info('Renaming All recieved Files')
    l=[]
    for i in d:
        if i in crc_bytes:
            p=subprocess.run(['mv',d[i],crc_bytes[i]])
            l.append(crc_bytes[i])
    j=0
    logging.info('removing one file')
    for files in os.listdir():
        if files not in l:
            p=subprocess.run(['rm',files])
            j=j+1
    if j==1:
        logging.info("One File is deleted. Everything Ok. ")
    join(path=r'/home/shivam/Work/Projects/test/server/s_split')
    logging.info("Move dowaloaded.bytes to server directory")
    p=subprocess.run(['mv','downloaded.bytes',r'/home/shivam/Work/Projects/test/server/'])  
    logging.info('Splited Files Deleted')
    for files in os.listdir():
        p=subprocess.run(['rm',files]) 
    logging.info("Changing Directory to server")
    set_directory(path=r'/home/shivam/Work/Projects/test/server/')
    final_stuff=frombytes(pstuff=fromdisk(path=os.getcwd(),filenm='downloaded.bytes'))
    logging.info("Writting The file as send.")
    todisk(stufft=final_stuff,dir=os.getcwd(),name='download.mp4')
    p=subprocess.run(['md5sum','download.mp4'],stdout=subprocess.PIPE)
    p=subprocess.run(['rm','downloaded.bytes'])
    if str(p.stdout)==serv.crc:
        logging.info("Files Downloaded Succesfully./nRemoving all the files ")
        