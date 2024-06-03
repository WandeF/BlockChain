# coding:utf-8
import json
import os
from filelock import FileLock

global BASEDBPATH
BLOCKFILE = 'blockchain'
UNTXFILE = 'untx'
NODEFILE = 'node'
SIGNFILE = 'sign'
CACHEFILE = 'cache'
PSIGNFILE = 'psign'


def set_file_path(config):
    global BASEDBPATH
    BASEDBPATH = config.get("data_path")


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True


def tryLock(file, timeout=3):
    locker = FileLock(file)
    try:
        locker.acquire(timeout)
        return True
    except Exception as e:
        return False


def tryUnLock(file):
    locker = FileLock(file)
    try:
        locker.release()
        return True
    except Exception as e:
        return False


def checksignal(db):
    psigndb = PsignDB()
    psign_path = psigndb.get_path()
    while tryLock(psign_path) == False:
        continue
    signdb = SignDB()
    sign = signdb.read()
    tryUnLock(psign_path)
    for i in sign:
        return i[db]


def setsignal(db, int):
    psigndb = PsignDB()
    psign_path = psigndb.get_path()
    while tryLock(psign_path) == False:
        continue
    signdb = SignDB()
    sign = signdb.read()
    for i in sign:
        i[db] = int
        signdb.clear()
        signdb.insert(i)
        tryUnLock(psign_path)


class BaseDB():
    filepath = ''

    def __init__(self):
        self.set_path()
        self.filepath = '/'.join((BASEDBPATH, self.filepath))

    def set_path(self):
        pass

    def get_path(self):
        return self.filepath

    def find_all(self):
        return self.read()

    def insert(self, item):
        self.write(item)

    def sread(self):
        raw = ''
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, 'r+') as f:
            raw = f.readline()
        return raw

    def read(self):
        dicts = []
        with open(self.filepath, 'r') as f:
            # with open(self.filepath, encoding='utf-8-sig', errors='ignore') as f:
            for line in f:
                # 去除行末的换行符
                line = line.strip()
                # 解析 JSON 字符串为字典对象
                #cprint('print', 'line: %s' % (str(line, )))
                try:
                    data = json.loads(line)
                except json.JSONDecodeError:
                    continue
                dicts.append(data)
        return dicts

    def write(self, item):
        with open(self.filepath, 'a') as f:
            json.dump(item, f)
            f.write('\n')
        return True


    def clear(self):
        with open(self.filepath, 'w+') as f:
            f.write('')

    def hash_insert(self, item):
        exists = False
        for i in self.find_all():
            if item['hash'] == i['hash']:
                exists = True
                break
        if not exists:
            self.write(item)


class NodeDB(BaseDB):

    def set_path(self):
        self.filepath = NODEFILE


class SignDB(BaseDB):

    def set_path(self):
        self.filepath = SIGNFILE


class PsignDB(BaseDB):

    def set_path(self):
        self.filepath = PSIGNFILE


class BlockChainDB(BaseDB):

    def set_path(self):
        self.filepath = BLOCKFILE

    def last(self):
        bc = self.read()
        if len(bc) > 0:
            return bc[-1]
        else:
            return []

    def find(self, hash):
        one = {}
        for item in self.find_all():
            if item['hash'] == hash:
                one = item
                break
        return one

    def insert(self, item):
        self.hash_insert(item)


class UnTransactionDB(BaseDB):
    """
    Transactions that doesn't store in blockchain.
    """

    def set_path(self):
        self.filepath = UNTXFILE

    def all_hashes(self):
        hashes = []
        for item in self.find_all():
            hashes.append(item['hash'])
        return hashes


class CacheDB(BaseDB):

    def set_path(self):
        self.filepath = CACHEFILE
