try:
   import os,pickle,sys,pickle,gzip,logging,time,subprocess
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    pass
class Network():
    def __init__(self,path,file):
        logging.info("Initalizing Attributes(Network)")
        self.path=path+r'/'
        self.file=file
        self.stuff=None
        self.crc=None
        self.file_no=None
        logging.info("Attributes Initialized(Network)")
    #open the file to send.
    def open(self): 
    	try:
    		logging.info("Opening File")        
    		with open(self.path+self.file,'rb') as infile:
    			logging.info("Reading File")
    			self.stuff=infile.read()
    	except IOError as e:
    		logging.info("Cannot Open: ")
    		logging.exception(e)
    	finally:
    		logging.info("File read with the size of: "+str(self.sz())+" MB")
    		infile.close()
    		logging.info("Closing File")
    #returns serialized item passed in as a parameter
    def tobytes(self): 
    	try:
    		self.stuff=pickle.dumps(self.stuff)
    	except pickle.PicklingError as e:
    		logging.info("Error in Serialisation of the Object. Object could not be converted to byetes. Make Sure the Datatype supports serialization.")
    		logging.exception(e)
    	finally:
        	print("Cpickle has Serialized: "+str(self.sz())+ " MB")
    #returns deserialized item passed in as a parameter
    def frombytes(self): 
        try:
            logging.info("Serializing stuff")
            self.stuff=pickle.loads(self.stuff)
        except pickle.UnpicklingError as e:
            logging.info("Error in Deserialisation of the Object. Object could not be converted to bytes.\nMake Sure the Datatype supports serialization.\n")
            logging.exception(e)
        finally:
            logging.info("Cpickle has DeSerialized: "+str(self.sz())+ " MB")
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
    def sz(self):
        logging.info("Calculating Size of Stuff")
        return sys.getsizeof(self.stuff)/1024**2
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
    def write(self,name):
        nf=True
        logging.info("Attempt to write file")
        try:
            with open(name,'wb') as outfile:
                outfile.write(self.stuff)
        except IOError as e:
            nf=False
            logging.error("Cannot write file to disk.")
            logging.exception(e)
        finally:
            if nf:
                logging.info("File written witten with size: "+str(self.sz())+" MB")
            outfile.close()
    #to Split the file into small chunks
    def split(self, chunk):        
        try:
            logging.info("Creating Directory")
            p=subprocess.run(['mkdir','split'])
            logging.info("Spliting the Files into %s parts: " %chunk)
            p=subprocess.run(['split','-b',chunk,self.path+self.file,os.getcwd()+r'/split/'+'part_'])
        except subprocess.CalledProcessError as err:
            logging.error("Cannot Split the file. Program Exit."+str(p))
            os._exit(0)
        finally:
            logging.info("Files split Succesfully")
    #to calculate the number of files splited
    def file_n(self):
        nf=True
        t=os.getcwd()
        print(t)
        try:
            logging.info("Entering Directory to count number of files ")
            os.chdir(t+'/split')            
        except:
            nf=False
            logging.error('Cannot enter into Directory.')
        finally:
            if nf:
                self.file_no=len(os.listdir())
                logging.info("Files calulcated.\nExit Directory to count number of files ")
                os.chdir(t)
    #to calculate the Check sum of the file
    def crc_n(self):W
        nf=True
        try:
            logging.info("Attempting to Find Check Sum of stuff: ")
            p=subprocess.check_output(['cksum',self.file])
        except subprocess.CalledProcessError as err:
            nf=False
            logging.error('Error at finding Check Sum of file. \n'+err)
        finally:
            if not nf:
                return
            logging.info("Check Sum Found")
            op=p.decode('utf-8').split(' ')
            op=op[0]+' '+op[1]
            self.crc=''.join(op)
    #to find crc and file number from handhsake
    def find_crc_fno(self,data):
        logging.info('Decoding data for CRC and File Numbers')
        data=data.decode('utf-8').split('/\\')
        file_no=int(data[1])
        data=data[0].split(' ')
        crc=data[0]+' '+data[1]
        logging.info('Data decoded for CRC and File Numbers')
        return crc,file_no    