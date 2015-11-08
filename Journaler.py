import hashlib
import os
import cPickle
import time
import csv
import errno
import json

class Journaler:
    '''
    Plan of Action:
    + The queuer receives a generator which is a pipe that comes all the way from the source file
    + The generator has items that are already conformant to the receiving Ring schema

    + The queuer exist to decouple the runtime between preparing the items and posting them to the Ring
    + If there is a catastropic failure, the queue should be able to continue where it left.
    + If the Ring rejects posting an item, there should be a record that keeps track of items that need to be revised
    '''

    def __init__(self,agent):

        self.AI_agent = agent
        self.taskname = str(int(time.time()))
        self.journal_root = 'Journal/'
        self.make_sure_path_exists(self.journal_root)

        
        self.count = {}

        #Initialize Journal
        

        #journal = open('journal_'+self.taskname+'.pkl','wb')  
        #journal = self.write_to_file('journal_'+self.taskname+'.pkl','wb')
        with open(self.journal_root+'journal_'+self.taskname+'.pkl','wb') as journal:
            j = {}
            cPickle.dump(j,journal)
        
        #journal.close()


    def make_sure_path_exists(self,path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise


    def set(self,item,status):
     
        line = {'s':status,'t':time.time()}

        if '_error' in item:
            line['e']=item['error']
            del item['_error']

        if '_msg' in item:
            line['msg']=item['_msg']
            del item['_msg']

        if '_uri' in item:
            line['uri']=item['_uri']
            del item['_uri']

        item_hash = hashlib.md5(repr(item)).hexdigest() 

        if status == 'invalid':
            # Write item to invalid_items file
            line['item'] = item         
            self.write_to_file(self.journal_root+'invalid_items_'+self.taskname+'.txt','a',json.dumps(line))

        if status == 'posted':
            self.write_to_file(self.journal_root+'posted_items_'+self.taskname+'.txt','a',json.dumps(line))
                
        try:
            #Retrieve journalfile
            j = {}

            with open(self.journal_root+'journal_'+self.taskname+'.pkl', 'rb+') as f:

                self.increase_count(status)
         
                #journal = open('journal_'+self.taskname+'.pkl', 'wb+')
                j = cPickle.load(f)
                print('UNPickling the following:',j)
                       

                #Modify journalfile
                if status == 'new':
                    if item_hash in j:
                        self.write_to_file(self.journal_root+'repeated_items_'+self.taskname+'.txt','a',repr(line)+' '+repr(item))
                        print('Repeated item! Ignoring it')
                        self.increase_count('repeated')
                        return False
                             
            j[item_hash] = line

            with open(self.journal_root+'journal_'+self.taskname+'.pkl', 'wb+') as f:

                #Save journalfile
                #journal = open('journal_'+self.taskname+'.pkl','wb')
                #cPickle.dump(j,journal)
                print('Pickling the following:',j)
                cPickle.dump(j,f)
                #journal.close()


            
          
            print(status,self.count[status],line)
            return True
      
        except EOFError,e:

            self.increase_count('journalingfailed')  #This is a Journal Error not a Post error
            print('ERROR',self.count[status],line)

            return False


            
    def write_to_csv(self,path,mode,line):

        with open(path,mode) as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow(line)

    def write_to_file(self,path,mode,line=None):

        with open(path,mode) as f:
            if line:
                f.write("%s\n" % line)




    def increase_count(self,status):

        if status not in self.count:
            self.count[status] = 1
        else:
            self.count[status] += 1


    def get(self,item):

        journal = open(self.journal_root+'journal_'+self.taskname+'.pkl', 'rb')
        j = cPickle.load(journal)
        journal.close() 

        item_hash = hashlib.md5(repr(item)).hexdigest() 

        if item_hash in j:
            return j[item_hash]
        else:
            return False


    def clean(self):

        if os.path.isfile(self.journal_root+'map_'+self.taskname+'.pkl'):
            os.remove(self.journal_root+'map_'+self.taskname+'.pkl')

        if os.path.isfile(self.journal_root+'journal_'+self.taskname+'.pkl'):
            os.remove(self.journal_root+'journal_'+self.taskname+'.pkl')






        
