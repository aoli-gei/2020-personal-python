import json
import os
import argparse
import multiprocessing
import shutil
import time
import sqlite3

class Data:
    def __init__(self, dict_address: int = None, reload: int = 0): #定义data类的构造方法
        localtime = time.asctime( time.localtime(time.time()) )
        print(localtime)
        if reload == 1:
            try:
                os.makedirs('json_save')
            except:
                # os.remove('json_1')     #无法删除
                shutil.rmtree('json_save')  # 可以
                os.makedirs('json_save')
            self.__init(dict_address)
        if dict_address is None and not os.path.exists('1.json') and not os.path.exists('2.json') and not os.path.exists('3.json'):
            raise RuntimeError('error: init failed')
        x = open('1.json', 'r', encoding='utf-8').read()
        self.__4Events4PerP = json.loads(x)
        x = open('2.json', 'r', encoding='utf-8').read()
        self.__4Events4PerR = json.loads(x)
        x = open('3.json', 'r', encoding='utf-8').read()
        self.__4Events4PerPPerR = json.loads(x)

    def __init(self, dict_address: str):
        json_list = [] #定义了一个列表
        self.__4Events4PerP = {}  #每一个人的四个项目
        self.__4Events4PerR = {}  #每个项目的四个项目
        self.__4Events4PerPPerR = {}  #每个人的每个项目的四个项目
        
        for root, dic, files in os.walk(dict_address):  #os.walk用来遍历一个目录内各个子目录和子文件
            pool = multiprocessing.Pool(processes=8)
            for f in files: #遍历整个文件夹的文件
                #self.write1(f,dict_address)
                pool.apply_async(self.write1,args=(f,dict_address))
            pool.close()
            pool.join()
        for root, dic, files in os.walk(dict_address):
                for f in files:  # 找格式文件
                    if f[-5:] == '.json':
                        x = open('json_save\\' + f,
                                 'r', encoding='utf-8').read()
                        x= json.loads(x)
                        self.count(x)
        '''
                if f[-5:] == '.json':   #如果文件的后缀为.json
                    json_path = f       #json_path记录下文件的地址
                    x = open(dict_address+'\\'+json_path,  #打开json文件，并返回文件对象（字符串），用只读方式，文件的指针默认放在文件开头
                             'r', encoding='utf-8').read()  #读文件，这里应该要改成readline，一次只读取一行，不然可能会裂开
                    str_list = [_x for _x in x.split('\n') if len(_x) > 0]#定义了一个列表，把每一行都加入到列表中去，split通过指定分隔符对字符串进行分片，这里用的回车，所以就按行分
                    for i, _str in enumerate(str_list):  #将这个str_list组合成一个索引序列
                        try:
                            json_list.append(json.loads(_str))  #在列表末尾添加对象
                        except:
                            pass  #防止出错
                records = self.__listOfNestedDict2ListOfDict(json_list)  #把这个列表变成字典
                json_list.clear()
                for i in records:
                    if not self.__4Events4PerP.get(i['actor__login'], 0):  #每个人四个事件的数量
                        self.__4Events4PerP.update({i['actor__login']: {}})
                        self.__4Events4PerPPerR.update({i['actor__login']: {}})
                    self.__4Events4PerP[i['actor__login']][i['type']
                                                ] = self.__4Events4PerP[i['actor__login']].get(i['type'], 0)+1
                    if not self.__4Events4PerR.get(i['repo__name'], 0):  #每个项目四个事件的数量
                        self.__4Events4PerR.update({i['repo__name']: {}})
                    self.__4Events4PerR[i['repo__name']][i['type']
                                            ] = self.__4Events4PerR[i['repo__name']].get(i['type'], 0)+1
                    if not self.__4Events4PerPPerR[i['actor__login']].get(i['repo__name'], 0): #每个人在每个项目
                        self.__4Events4PerPPerR[i['actor__login']].update({i['repo__name']: {}})
                    self.__4Events4PerPPerR[i['actor__login']][i['repo__name']][i['type']
                                                                ] = self.__4Events4PerPPerR[i['actor__login']][i['repo__name']].get(i['type'], 0)+1
                    '''
        localtime = time.asctime( time.localtime(time.time()) )
        print(localtime)
        with open('1.json', 'w', encoding='utf-8') as f:  #打开，并写入
            json.dump(self.__4Events4PerP,f)
        with open('2.json', 'w', encoding='utf-8') as f:  #打开，并写入
            json.dump(self.__4Events4PerR,f)
        with open('3.json', 'w', encoding='utf-8') as f:  #打开，并别入
            json.dump(self.__4Events4PerPPerR,f)
                #上面这些看不懂

    def count(self,records):
        print("counting...")
        print(os.getppid())
        for i in records:
            if not self.__4Events4PerP.get(i['actor__login'], 0):  #每个人四个事件的数量
                self.__4Events4PerP.update({i['actor__login']: {}})
                self.__4Events4PerPPerR.update({i['actor__login']: {}})
            self.__4Events4PerP[i['actor__login']][i['type']
                                        ] = self.__4Events4PerP[i['actor__login']].get(i['type'], 0)+1
            if not self.__4Events4PerR.get(i['repo__name'], 0):  #每个项目四个事件的数量
                self.__4Events4PerR.update({i['repo__name']: {}})
            self.__4Events4PerR[i['repo__name']][i['type']
                                    ] = self.__4Events4PerR[i['repo__name']].get(i['type'], 0)+1
            if not self.__4Events4PerPPerR[i['actor__login']].get(i['repo__name'], 0): #每个人在每个项目
                self.__4Events4PerPPerR[i['actor__login']].update({i['repo__name']: {}})
            self.__4Events4PerPPerR[i['actor__login']][i['repo__name']][i['type']
                                                        ] = self.__4Events4PerPPerR[i['actor__login']][i['repo__name']].get(i['type'], 0)+1
    
    def write1(self,f,dict_address):  #用来多进程读入
        print("writing....")
        print(os.getppid())
        json_list=[]
        if f[-5:] == '.json':   #如果文件的后缀为.json
            json_path = f       #json_path记录下文件的地址
            x = open(dict_address + '\\' + json_path, 'r', encoding='utf-8')
            with mmap.mmap(x.fileno(), 0, access=mmap.ACCESS_READ) as m:
                m.seek(0, 0)
                obj = m.read()
                obj = str(obj, encoding="utf-8")
                str_list = [_x for _x in obj.split('\n') if len(_x) > 0]
                for i, _str in enumerate(str_list):
                    try:
                        json_list.append(json.loads(_str))
                    except:
                        pass
            self.save(json_list,f)
            
    def save(self,json_list,f1):
        print("saving...")
        print(os.getppid())
        record = self.__listOfNestedDict2ListOfDict(json_list)
        k=[]
        for i in record:
            k.append({'actor__login':i['actor__login'],'type':i['type'],'repo__name':i['repo__name']})
        with open('json_save\\'+f1, 'w', encoding='utf-8') as f:  # 初始化
            json.dump(k, f)  # 写入


    def __parseDict(self, d: dict, prefix: str):  #用于与底下的函数配合来将列表转换为字典，所以不用动这两个
        _d = {}
        for k in d.keys():
            if str(type(d[k]))[-6:-2] == 'dict':
                _d.update(self.__parseDict(d[k], k))
            else:
                _k = f'{prefix}__{k}' if prefix != '' else k
                _d[_k] = d[k]
        return _d

    def __listOfNestedDict2ListOfDict(self, a: list):  #用于转换
        records = []
        for d in a:
            _d = self.__parseDict(d, '')
            records.append(_d)
        return records

    def getEventsUsers(self, username: str, event: str) -> int:
        if not self.__4Events4PerP.get(username,0):
            return 0
        else:
            return self.__4Events4PerP[username].get(event,0)

    def getEventsRepos(self, reponame: str, event: str) -> int:
        if not self.__4Events4PerR.get(reponame,0):
            return 0
        else:
            return self.__4Events4PerR[reponame].get(event,0)

    def getEventsUsersAndRepos(self, username: str, reponame: str, event: str) -> int:
        if not self.__4Events4PerP.get(username,0):
            return 0
        elif not self.__4Events4PerPPerR[username].get(reponame,0):
            return 0
        else:
            return self.__4Events4PerPPerR[username][reponame].get(event,0)

#低下这些应该是命令行的操作
class Run:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.data = None
        self.argInit()
        print(self.analyse())

    def argInit(self):
        self.parser.add_argument('-i', '--init')
        self.parser.add_argument('-u', '--user')
        self.parser.add_argument('-r', '--repo')
        self.parser.add_argument('-e', '--event')

    def analyse(self):
        if self.parser.parse_args().init:
            self.data = Data(self.parser.parse_args().init, 1)
            return 0
        else:
            if self.data is None:
                self.data = Data()
            if self.parser.parse_args().event:
                if self.parser.parse_args().user:
                    if self.parser.parse_args().repo:
                        res = self.data.getEventsUsersAndRepos(
                            self.parser.parse_args().user, self.parser.parse_args().repo, self.parser.parse_args().event)
                    else:
                        res = self.data.getEventsUsers(
                            self.parser.parse_args().user, self.parser.parse_args().event)
                elif self.parser.parse_args().repo:
                    res = self.data.getEventsRepos(
                        self.parser.parse_args().repo, self.parser.parse_args().event)
                else:
                    raise RuntimeError('error: argument -l or -c are required')
            else:
                raise RuntimeError('error: argument -e is required')
        return res


if __name__ == '__main__':
    a = Run()