class MempoolTransaction():
    def __init__(self, txid, fee, weight, parent):
        '''constructor'''
        self.txid=txid
        self.fee=int(fee)
        self.weight=int(weight)
        self.parent = parent

class Block():
    '''
    creating blocks of valid 
    mempool transactions
    '''
    def __init__(self, txid, fee, weight):
        self.txid=txid
        self.fee=int(fee)
        self.weight=int(weight)


class BlockChain():
    '''
    the final blockchian
    for printning later.
    '''

    def __init__(self, todo_list):
        '''constructor'''
        self.chain=[]
        self.todo_list=todo_list
        self.max_allowed_weight = 4000000


    def priorityFunction(self, mempool_transaction_object):
        '''
        a and b are arbitary constants for optimization
        to create a prority function which maximize the
        fee and minimize the weight.
        '''
        a = 1
        b = 100
        return a*mempool_transaction_object.fee+b/mempool_transaction_object.weight


    def parentInTodo(self, mempool_transaction_object):
        '''
        Helper function to find if a mempool transaction
        object's parent in present in the chain, only then
        will the program append it to the chain.
        ''' 
        for chain_index in range(len(self.chain)):
            if(self.chain[chain_index].txid==mempool_transaction_object.parent):
                return True        
        return False
        
    def appendToChain(self, mempool_transaction_object):
        '''
        creating a block and adding
        it to blockchain
        '''
        block = Block(mempool_transaction_object.txid, 
                                        mempool_transaction_object.fee, 
                                        mempool_transaction_object.weight)
        self.chain.append(block)

    def maximizeFee(self):
        '''append to blockchain and find order of transactions for maximum fees'''

        avg_priority = (sum([self.priorityFunction(mem_obj) for mem_obj in self.todo_list]))/len(self.todo_list)
        #calculating average priority of entier todo_list to compare with each element later

        total_weight = 0
        #intializing total weight to 0 to check if transactions don't exceed the given amount
        
        self.todo_list = sorted(self.todo_list, key=lambda mem_obj: mem_obj.fee, reverse=True)
        #sorting todo_list by decreasing order of fee to maximize earnings

        for todo_index in range(len(self.todo_list)):

            if(self.priorityFunction(self.todo_list[todo_index])>avg_priority):
            #comparing priority function of that index with average priority

                if len(self.todo_list[todo_index].parent) == 0:
                #checking if the mempool_transaction_object has parents

                    self.appendToChain(self.todo_list[todo_index])
                    total_weight=total_weight+self.todo_list[todo_index].weight

                else:
                    if self.parentInTodo(self.todo_list[todo_index]):
                    #checking if parents in the chain
                                            
                        self.appendToChain(self.todo_list[todo_index])
                        total_weight=total_weight+self.todo_list[todo_index].weight

            if total_weight>self.max_allowed_weight:
            #checking if maximum weight is not violated

                self.chain.pop()
                #removing last element added to chain which violated max_allowed_weight

                return

    def printChain(self):
        '''
        print the chain to block.txt file
        '''
        with open("block.txt", "w") as file:
            for line in self.chain:
                file.write(line.txid)
                file.write("\n")


def ParseMempoolCsv():
    '''
    Parse the CSV file and return a list of MempoolTransactions.
    '''
    with open('mempool.csv') as f:
        return([MempoolTransaction(*line.strip().split(',')) for line in f.readlines()])

def main():
    todo_list = ParseMempoolCsv()
    blockchain = BlockChain(todo_list)
    blockchain.maximizeFee()
    blockchain.printChain()

if __name__ =="__main__":
    main()