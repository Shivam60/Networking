try:
   import os,pickle,sys,pickle,gzip,logging,time,subprocess
except ImportError as e:
   print("Importing Failed, Make sure the Requirements are met. Program exiting:\n"+e)
   os._exit(0)
finally:
    pass

#open the file to send.
def openf(path,filenm): 
    nf=True
    path=path+filenm
    try:
        logging.info("Opening File")        
        infile= open(path,'rb')
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
            return stuff
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
def find_crc_fno(data):
    logging.info('Decoding data for CRC and File Numbers')
    data=data.decode('utf-8').split('/\\')
    file_no=int(data[1])
    data=data[0].split(' ')
    crc=data[0]+' '+data[1]
    logging.info('Data decoded for CRC and File Numbers')
    return crc,file_no
#write file to disk with a supplied name
def write(stufft,name,dir):
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
            outfile.close()
            os.chdir(t)
        outfile.close()

#to Split the file into small chunks
def split(path,filenm,chunk='3M'):
    try:
        logging.info("Spliting the Files into %s parts: " %chunk)
        p=subprocess.run(['split','-b',chunk,filenm,path])
    except subprocess.CalledProcessError as err:
        logging.error("Cannot Split the file. Program Exit.\n"+str(p))
        os._exit(0)
    finally:
        logging.info("Files split Succesfully")
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
    def find_crc_fno(self,data):
        logging.info('Decoding data for CRC and File Numbers')
        data=data.decode('utf-8').split('/\\')
        file_no=int(data[1])
        data=data[0].split(' ')
        crc=data[0]+' '+data[1]
        logging.info('Data decoded for CRC and File Numbers')
        return crc,file_no
    #to join smaller files into single file
    def join(self,name):
        try:
            logging.info("Joining the Files into %s parts: " %chunk)
            p=subprocess.run(['split','-b',chunk,self.path+self.file,os.getcwd()+r'/split/'+'part_'])
        except subprocess.CalledProcessError as err:
            logging.error("Cannot Split the file. Program Exit.\n"+str(p))
            os._exit(0)
        finally:
            logging.info("Files split Succesfully")
#to set the current working directory
def set_directory(path):
    try:
        logging.info("Chaning the Directory: ")
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