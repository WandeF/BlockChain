# coding:utf-8

from xmlrpc.client import ServerProxy
from blockchain.database import *
from blockchain.lib.common import cprint

server = None

PORT = 8301


class RpcServer:

    def __init__(self, serversimple, config):
        self.server = serversimple
        set_file_path(config)

    def ping(self):
        return True

    def get_blockchain(self):
        while (checksignal('blockchain') != 0):
            continue
        setsignal('blockchain', 1)
        bcdb = BlockChainDB()
        bc = bcdb.find_all()
        setsignal('blockchain', 0)
        return bc

    def get_sign(self):
        signdb = SignDB()
        return signdb.find_all()

    def new_block(self, block):
        psign_path = PsignDB().get_path()
        # cprint('INFO', "Receive new block.")
        while tryLock(psign_path) == False:
            continue
        # cprint('RPC', block)
        # cprint('RPC', "Cache: Start inserting")
        CacheDB().insert(block)
        # cprint('RPC', "Cache: Finished")
        tryUnLock(psign_path)
        return True

    def add_node(self, address):
        add_node(address)
        return True


class RpcClient:
    ALLOW_METHOD = ['get_blockchain', 'get_sign', 'new_block', 'ping', 'add_node']

    def __init__(self, node):
        self.node = node
        self.client = ServerProxy(node)

    def __getattr__(self, name):
        def noname(*args, **kw):
            if name in self.ALLOW_METHOD:
                return getattr(self.client, name)(*args, **kw)

        return noname


class BroadCast:

    def __init__(self):
        # 只在构造的时候，打开node文件（只打开一次）获取node并构建clients，
        self.clients = get_clients()

    def __getattr__(self, name):
        def noname(*args, **kw):
            rs = []
            for c in self.clients:
                try:
                    # c是方法，name是消息
                    rs.append(getattr(c, name)(*args, **kw))
                except ConnectionRefusedError:
                    cprint('WARN', 'Contact with node %s failed when calling method %s , please check the node.' % (
                        c.node, name))
                else:
                    # cprint('INFO', 'Contact with node %s successful calling method %s .' % (c.node, name))
                    pass
            # cprint('INFO', 'rs %s .' % rs)
            return rs

        return noname


def get_clients():
    clients = []
    nodes = get_nodes()  # [['http://127.0.0.1:3003']]

    for node in nodes:
        # 根据node文件中的node，获取所有的、对应的RPCclients
        clients.append(RpcClient(node))  # 使用索引来获取节点字符串
    return clients


def get_nodes():
    nodes = NodeDB().find_all()
    nodes = list(nodes)
    return nodes


def add_node(address):
    ndb = NodeDB()
    all_nodes = ndb.find_all()
    if address.find('http') != 0:
        address = 'http://' + address
    all_nodes.append(address)
    ndb.clear()
    ndb.write(rm_dup(all_nodes))
    return address


def rm_dup(nodes):
    return sorted(set(nodes))
