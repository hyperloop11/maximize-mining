# maximize-mining

This python project parses the mempool.csv file which has parameters:
1. txid: the transaction identifier
2. fee: transaction fee
3. weight: weight of trasnaction
4. parent_txids: list of txid of its parents

# The problem

To find a solution, we have to find an order in which to make valid blocks, such that fees obtained was maximized and the total weight of the transactions never exceeded a certain number. Also a trasnsaction is only processed if all its parents are processed first.

# The solution

1. The solution I came up with firstly sorts the list of transactions in decreasing order of fee, so that the transactions with maximum fees are processed first.

2. Secondly, creating an optimization function, which increases a transaction's priority if its fees is more and weight is less.

3. Lastly, added the confirmed transactions to a blockchain to maximize the total fee obtained by the miner.
