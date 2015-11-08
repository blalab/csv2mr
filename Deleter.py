class Deleter:
    

    def __init__(self,agent):
        self.AI_agent = agent 
        self.journal_root = 'Journal/'
        


    def delete(self,uri):

        payload = {'method':'delete'}
        r = requests.delete(self.target,data=payload)

        print(r.status_code)
        print(r.headers)
        print('TEXT:',r.text)

        return r

    def unpost(self):

        taskname = raw_input('What task you want to unpost?')

        with open(self.journal_root+'posted_items_'+taskname+'.txt', 'rb+') as f:

            

            for line in f:
                print(line)
                print('DELETE',line['uri'])
                # self.delete()


if __name__ == '__main__':

    dl = Deleter('AVISPA')
    dl.unpost()



