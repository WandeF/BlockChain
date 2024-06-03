"""
智能合约中间层
获取区块链数据，合约索引，数据索引，标志位访问
dalsim如何调用，主动轮询还是被动调用


"""
from blockchain.database import SignDB, BlockChainDB


class smartContract():
    def __init__(self, contract_index=1):
        """
        初始化智能合约
        """
        try:
            file = open("mycontract.pyc", 'rb')
            self.contract = file.read()
            file.close()
        except FileNotFoundError:
            print("not fount pyc file")
            self.contract = self.get_contract(contract_index)
            file = open("mycontract.pyc", 'wb')
            file.write(self.contract)
            file.close()
        self.data = []

    def get_contract(self, index):
        return b""
        pass

    def sumit_block(self, type):
        """
        提交区块,type =
        """
        if type == 1:
            # 传入传感器数据
            pass
        elif type == 2:
            # 提交决策结果
            pass
        elif type == 3:
            self.contractIndex = "1234"
            pass
        pass

    def check_contract(self):
        """
        检查区块链和本地代码
        """
        file = open("mycontract.pyc", 'wb')
        content = file.read()

        pass

    def run_contract(self):
        """
        运行合约，
        """
        import importlib.util
        while 1:
            if self.check_contract():
                pyc_file = './mycontract.pyc'
                spec = importlib.util.spec_from_file_location('content', pyc_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                a = 2000
                data = []
                bcdb = BlockChainDB()
                while --a:
                    data.append(bcdb.last() if bcdb.last() not in data else [])
                    result = module.main(data)
                    if result[0]:
                        continue
                    data = []


if __name__ == '__main__':
    bcdb = BlockChainDB()
    print(bcdb.last())
