import hashlib
import os
import cPickle
import time
import csv

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
        
        self.count = {}

        #Initialize Journal
        j = {}
        journal = open('journal_'+self.taskname+'.pkl','wb')  
        cPickle.dump(j,journal)
        journal.close()


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
            #self.create_file_if_exists_not('invalid_items_'+self.taskname+'.txt')
            self.write_to_file('invalid_items_'+self.taskname+'.txt','a',repr(line)+' '+repr(item))

        if status == 'posted':
            self.write_to_file('posted_items_'+self.taskname+'.txt','a',repr(line)+' '+repr(item))
                
        try:
            #Retrieve journalfile
            j = {}

            with open('journal_'+self.taskname+'.pkl', 'rb+') as f:

                self.increase_count(status)
         
                #journal = open('journal_'+self.taskname+'.pkl', 'wb+')
                j = cPickle.load(f)
                print('UNPickling the following:',j)
                       

                #Modify journalfile
                if status == 'new':
                    if item_hash in j:
                        print('Repeated item! Ignoring it')
                        self.increase_count('repeated')
                        return False
                             
            j[item_hash] = line

            with open('journal_'+self.taskname+'.pkl', 'wb+') as f:

                #Save journalfile
                #journal = open('journal_'+self.taskname+'.pkl','wb')
                #cPickle.dump(j,journal)
                print('Pickling the following:',j)
                cPickle.dump(j,f)
                #journal.close()


            
          
            print('OK',self.count[status],line)
            return True
      
        except EOFError,e:

            self.increase_count('journalingfailed')  #This is a Journal Error not a Post error
            print('ERROR',self.count[status],line)

            return False

    def create_file_if_exists_not(self,path):

        if not os.path.isfile(path): 
            #Create the file
            open(path,'w')
                

    def write_to_csv(self,path,mode,line):

        with open(path,mode) as f:
                    writer = csv.writer(f,delimiter=",")
                    writer.writerow(line)

    def write_to_file(self,path,mode,line):

        with open(path,mode) as f:
            f.write("%s\n" % line)



    def increase_count(self,status):

        if status not in self.count:
            self.count[status] = 1
        else:
            self.count[status] += 1


    def get(self,item):

        journal = open('journal_'+self.taskname+'.pkl', 'rb')
        j = cPickle.load(journal)
        journal.close() 

        item_hash = hashlib.md5(repr(item)).hexdigest() 

        if item_hash in j:
            return j[item_hash]
        else:
            return False


    def clean(self):

        if os.path.isfile('map_'+self.taskname+'.pkl'):
            os.remove('map_'+self.taskname+'.pkl')

        if os.path.isfile('journal_'+self.taskname+'.pkl'):
            os.remove('journal_'+self.taskname+'.pkl')






        
