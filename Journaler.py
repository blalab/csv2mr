
class Journaler:
    '''
    Plan of Action:
    + The queuer receives a generator which is a pipe that comes all the way from the source file
    + The generator has items that are already conformant to the receiving Ring schema

    + The queuer exist to decouple the runtime between preparing the items and posting them to the Ring
    + If there is a catastropic failure, the queue should be able to continue where it left.
    + If the Ring rejects posting an item, there should be a record that keeps track of items that need to be revised
    '''

    def __init__(self,agent,taskname):

        self.AI_agent = agent
        self.taskname = taskname
        self.count = 0
        self.count_ok = 0
        self.count_error = 0

        j = ['START']
        journal = open('journal_'+taskname+'.pkl','wb')  
        cPickle.dump(j,journal)
        journal.close()

        journal = open('journal_'+taskname+'.pkl', 'rb')
        j = cPickle.load(journal)
        print(j)
        journal.close()


    def insert(self,item):

        self.count += 1
              
        try:
            journal = open('journal_'+self.taskname+'.pkl', 'rb')
            j = cPickle.load(journal)
            journal.close()
            #Append new entry to journal
            j.append(item)
        
            #Save to journalfile
            journal = open('journal_'+self.taskname+'.pkl','wb')
            cPickle.dump(j,journal)
            journal.close()
            print('OK',self.count,item)
            self.count_ok += 1
      
        except EOFError,e:
            self.count_error += 1
            print('EOFError',self.count,item)

    def close(self):

        journal = open('journal_'+self.taskname+'.pkl', 'rb')
        j = cPickle.load(journal)
        journal.close()
        j.append(['END'])

        #Save to journalfile
        journal = open('journal_'+self.taskname+'.pkl','wb')
        cPickle.dump(j,journal)
        journal.close()



        
