# coding:utf-8
from blockchain.database import *
import multiprocessing
from xmlrpc.server import SimpleXMLRPCServer
from blockchain.rpc import RpcServer, BroadCast
from blockchain.lib.common import cprint
import yaml
from blockchain.mine import Miner


def load_config(file_path):
    with open(file_path, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            return config
        except yaml.YAMLError as exc:
            print(f"Error loading YAML file: {exc}")
            return None


def start_server(ip, port, config):
    simple_server = SimpleXMLRPCServer((ip, port))
    rpc_server = RpcServer(simple_server, config)
    simple_server.register_instance(rpc_server)
    simple_server.serve_forever()


class Node:
    def __init__(self, config_file):
        # 加载配置文件
        self.config = load_config(config_file)
        set_file_path(self.config)
        # 从配置文件中，读出ip和port
        self.ip_port = self.config.get("ip_address")
        self.port = self.ip_port[-4:]

        self.NodeDB = NodeDB()
        # node拥有自己的矿工miner
        self.miner = Miner()

    def start(self):
        self.start_node()
        self.miner.start_mine(self.port)

    def start_node(self):
        cprint('INFO', 'Node initialize success.')
        ip = ''
        port = ''
        ip_port = self.ip_port
        try:
            if ip_port.find('.') != -1:
                host, port = ip_port.split(':')
            else:
                host = '0.0.0.0'
                port = ip_port
        except Exception:
            cprint('ERROR', 'params must be {port} or {host}:{port} , ps: 3009 or 0.0.0.0:3009')
        p = multiprocessing.Process(target=start_server, args=(ip, int(port), self.config))
        p.start()
        cprint('INFO', 'Node start success. Listen at %s.' % (ip_port,))

    def init_node(self):
        """
        Download blockchain from node compare with local database and select the longest blockchain. 没有用，强行同步过去
        """
        all_node_blockchains = BroadCast().get_blockchain()
        # all_node_txs = rpc.BroadCast().get_transactions()
        bcdb = BlockChainDB()
        blockchain = bcdb.find_all()
        # If there is a blochain downloaded longer than local database then relace local's.
        for bc in all_node_blockchains:
            if len(bc) > len(blockchain):
                while (checksignal('blockchain') != 0):
                    continue
                setsignal('blockchain', 1)
                bcdb.clear()
                bcdb.write(bc)
                setsignal('blockchain', 0)
                print("Already exchanged!")


if __name__ == '__main__':
    nood3008 = Node('node3008.yaml')
    nood3008.start()
