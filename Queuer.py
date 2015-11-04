
class Queuer:
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

    def insert():

        pass
