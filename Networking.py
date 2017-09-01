try:
   import os,pickle,sys,pickle,gzip,logging,time,subprocess
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
class Network():
    def __init__(self,path):
        logging.info("Initalizing Attributes")
        self.path=path
        self.stuff=None
        logging.info("Attributes Initialized")
    def open(self): #open the file to send.
    	try:
    		logging.info("Opening File")        
    		with open(self.path,'rb') as infile:
    			logging.info("Reading File")
    			self.stuff=infile.read()
    	except IOError as e:
    		logging.info("Cannot Open: ")
    		logging.exception(e)
    	finally:
    		logging.info("File read with the size of: "+str(self.sz())+" MB")
    		infile.close()
    		logging.info("Closing File")
    def tobytes(self): #returns serialized item passed in as a parameter
    	try:
    		self.stuff=pickle.dumps(self.stuff)
    	except pickle.PicklingError as e:
    		logging.info("Error in Serialisation of the Object. Object could not be converted to byetes. Make Sure the Datatype supports serialization.")
    		logging.exception(e)
    	finally:
        	print("Cpickle has Serialized: "+str(self.sz())+ " MB")
    def frombytes(self): #returns deserialized item passed in as a parameter
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
    def split(self, chunk):        
        try:
            logging.info("Creating Directory")
            p=subprocess.run(['mkdir','split'])
            logging.info("Spliting the Files into %s parts: " %chunk)
            p=subprocess.run(['split','-b',chunk,self.path,os.getcwd()+r'/split/'+'part_'])
        except subprocess.CalledProcessError as err::
            logging.error("Cannot Split the file. Program Exit."+str(p))
            os._exit(0)
        finally:
            logging.info("Files split Succesfully")
    def file_no(self):
        nf=True
        try:
            logging.info("Entering Directory to count number of files ")
            os.chdir(os.getcwd()+'/split')
        except:
            nf=False
            logging.error('Cannot enter into Directory.')
        finally:
            if nf:
                return len(os.lisdir())
    def crc(self):
        nf=True
        try:
            logging.info("Attempting to Find Check Sum of stuff: ")
            p=subprocess.run(['cksum',''],stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as err:
            nf=False
            logging.error('Error at finding Check Sum of file. \n'+err)
        finally:
            if nf:
                return completed.stdout.decode('utf-8')
if __name__=="__main__":
	fl1=Network("2.bytes")
	fl1.open()            
	fl1.tobytes()
	fl1.split(chunk='5m')
