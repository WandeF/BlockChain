# coding:utf-8

from blockchain.block import Block
from blockchain.database import *

import time
from blockchain.rpc import BroadCast

MODULES = ['account', 'tx', 'blockchain', 'miner', 'node']


class Miner:
    def __init__(self):
        self.BlockChainDB = BlockChainDB()
        self.CacheDB = CacheDB()
        self.PsignDB = PsignDB()
        self.SignDB = SignDB()
        self.UnTransactionDB = UnTransactionDB()

        #self.BlockChainDB.clear()
        self.CacheDB.clear()
        self.PsignDB.clear()
        self.SignDB.clear()
        dict = {"blockchain": 0, "cache": 0}
        self.SignDB.write(dict)

        self.broadcast = BroadCast()

    def start_mine(self, node):
        while True:
            untxs = self.UnTransactionDB.find_all()
            self.onChain()
            if len(untxs)==0:
                continue
            else:
                # cprint('Miner new block',mine(node).to_dict())
                # 挖block
                chainblockDict = self.mine(node)
                # 广播出去
                self.broadcast.new_block(chainblockDict)


    def mine(self, node):
        """
        Main miner method.
        """
        # Found last block and unchecked transactions.
        psign_path = self.PsignDB.get_path()
        last_block = self.BlockChainDB.last()
        if len(last_block) == 0:
            last_block = self.coinbase().to_dict()
        untxs = self.UnTransactionDB.find_all()
        self.UnTransactionDB.clear()

        folder_path = os.path.dirname(psign_path)
        sign_path = os.path.join(folder_path, "tx")
        self.set_sign(sign_path, 1)

        # Miner reward is the first transaction.
        chainblock = Block(last_block['index'] + 1, time.time(), untxs, last_block['hash'], node)
        nouce = chainblock.pow()
        chainblock.make(nouce)
        # Save block and transactions to database.
        while tryLock(psign_path) == False:
            #cprint("shen","CacheDB insert locked")
            continue
        chainblockDict = chainblock.to_dict()
        #cprint('Miner', chainblockDict)
        #cprint('Miner', "CacheDB write start")
        self.CacheDB.insert(chainblockDict)
        #cprint('Miner', "CacheDB write end")
        tryUnLock(psign_path)
        #Block.spread(chainblockDict)
        #self.onChain()
        return chainblockDict

    def onChain(self):  # 对cache的blockchain进行检查，对满足时间的发到blockchain上
        psign_path = self.PsignDB.get_path()
        for i in range(2):
            while tryLock(psign_path) == False:
                continue

            cache = self.CacheDB.find_all()
            tryUnLock(psign_path)
            if len(cache) != 0:
                min_time = min(cache, key=lambda x: x['timestamp'])
            else:
                break
            if time.time() - min_time['timestamp'] > 5:
                min_time['index'] = self.BlockChainDB.last()['index'] + 1
                self.BlockChainDB.insert(min_time)
                while tryLock(psign_path) == False:
                    continue
                self.CacheDB.clear()
                for block in cache:  # 在cache中删已经添加到blockchain那一条数据
                    if block != min_time:
                        self.CacheDB.insert(block)
                tryUnLock(psign_path)
            else:
                break

    def coinbase(self):
        """
        First block generate.
        """
        # rw = reward()
        cb = Block(0, time.time(), "", "", "")
        nouce = cb.pow()
        cb.make(nouce)
        # Save block and transactions to database.
        self.BlockChainDB.insert(cb.to_dict())
        return cb

    def set_sign(self, sign_path, new_value):

        with open(sign_path, 'w') as f:
            f.write(str(new_value))
