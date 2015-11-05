import hashlib
import os
import cPickle
import time

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

        
        item_hash = hashlib.md5(repr(item)).hexdigest()      
        line = {'s':status,'t':time.time()}
                 
        try:
            #Retrieve journalfile
            journal = open('journal_'+self.taskname+'.pkl', 'rb')
            j = cPickle.load(journal)
            journal.close()          

            #Modify journalfile
            if status == 'new':
                if item_hash in j:
                    print('Repeated item! Ignoring it')
                    self.increase_count('repeated')
                    return False
                         
            j[item_hash] = line

            #Save journalfile
            journal = open('journal_'+self.taskname+'.pkl','wb')
            cPickle.dump(j,journal)
            journal.close()

            self.increase_count(status)
          
            print('OK',self.count[status],line)
            return True
      
        except EOFError,e:

            self.increase_count('failed')
            print('OK',self.count[status],line)

            return False

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






        
