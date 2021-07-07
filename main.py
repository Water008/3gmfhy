import time

import requests

from config import *
from encrypt import AesSample


class Garden:
    def __init__(self):
        self.sessionId = ''
        self.friendsId = {}
        self.potId = []
        self.JM = AesSample()
        self.EXP = True

    def time_stamp(self) -> int:
        return int(time.time() * 1000)

    def post_temple(self, url, data):
        info = requests.post(base_url + url, data=data, headers=headers)
        return info.json()

    def login(self):
        data = {'data': {'account': username, 'password': password}, 'checkTime': self.time_stamp()}
        login = self.post_temple(login_url, self.JM.encode(str(data)))
        if login['code'] == '200':
            print(login['data']['nick_name'], login['msg'])
            self.sessionId = login['sessionId']
            if self.sessionId != '':
                print('获取sessionId成功！')
        else:
            print(login['msg'])

    def sign(self):
        data = {'data': {'userId': self.sessionId}, 'checkTime': self.time_stamp()}
        sign = self.post_temple(sign_url, self.JM.encode(str(data)))
        print(sign['msg'])

    def oneOperation(self):
        data = {'data': {'userId': self.sessionId}, 'checkTime': self.time_stamp()}
        oneOperation = self.post_temple(oneOperation_url, self.JM.encode(str(data)))
        print(oneOperation['msg'])

    def oneHarvestFlower(self):
        data = {'data': {'userId': self.sessionId}, 'checkTime': self.time_stamp()}
        oneHarvestFlower = self.post_temple(oneHarvestFlower_url, self.JM.encode(str(data)))
        print(oneHarvestFlower['msg'])

    def sow(self, sow_type, flower_id):
        """
        :param flower_id: 种子的uuid
        :param sow_type: 1为种植一个，2为一键全种
        :return:
        """
        data = {'data': {'flower_id': str(flower_id), 'flower_name': seed_info[str(flower_id)], 'potId': self.potId[0],
                         'type': str(sow_type), 'userId': self.sessionId},
                'checkTime': self.time_stamp()}
        sow = self.post_temple(sow_url, self.JM.encode(str(data)))
        print(sow['msg'])

    def flowerpot(self):
        self.potId.clear()
        data = {'data': {'userId': self.sessionId}, 'checkTime': self.time_stamp()}
        flowerpot = self.post_temple(flowerpot_url, self.JM.encode(str(data)))
        for i in flowerpot['data']:
            self.potId.append(i['uuid'])
            print(i['flower_name'], i['surplusTime'], i['flower_stage'], i['is_insects'], i['is_water'], i['is_weed'])

    def add_seed(self, flower_id='1'):
        """
        :param flower_id: 种子的uuid
        :return:
        """
        data = {'data': {'flowerId': str(flower_id), 'userId': self.sessionId, 'num': buy_seed_num},
                'checkTime': self.time_stamp()}
        add_seed = self.post_temple(add_url, self.JM.encode(str(data)))
        print(add_seed['msg'])

    def getMyFriends(self):
        self.friendsId.clear()
        data = {"data": {"pageSize": "1", "pageNum": "2000", "type": "1",
                         "userId": self.sessionId}, "checkTime": self.time_stamp()}
        getMyFriends = self.post_temple(getMyFriends_url, self.JM.encode(str(data)))
        for i in getMyFriends['data']:
            if i['is_operation'] == 1:
                self.friendsId.update({i['nick_name']: i['friend_id']})
        print(self.friendsId)
        print(f"共{len(self.friendsId)}个可偷取好友")

    def getFriendsPot(self):
        for name, fid in self.friendsId.items():
            data = {"data": {"userId": fid}, "checkTime": self.time_stamp()}
            getFriendsPot = self.post_temple(getFriendsPot_url, self.JM.encode(str(data)))['data']
            for i in getFriendsPot:
                if self.EXP == True:
                    if i['is_weed'] == '0':
                        self.helpFriendOperation(fid, i['uuid'], '2', name, i['flower_name'])
                    if i['is_insects'] == '0':
                        self.helpFriendOperation(fid, i['uuid'], '3', name, i['flower_name'])
                if i['is_plant'] == "1" and i['surplusTime'] == None:
                    self.extractFlower(fid, i['uuid'], name, i['flower_name'])

    def helpFriendOperation(self, fid, fpotid, otype, name, flower_name):
        data = {"data": {"friendId": fid, "userId": self.sessionId, "potId": fpotid, "type": otype},
                "checkTime": self.time_stamp()}
        helpFriendOperation = self.post_temple(helpFriendOperation_url, self.JM.encode(str(data)))
        if otype == '1':
            lx = "浇水"
        elif otype == '2':
            lx = "除草"
        elif otype == '3':
            lx = "捉虫"
        print(f"帮助{name}的{flower_name}{lx} {helpFriendOperation['msg']}")
        if helpFriendOperation['msg'][-1] == "0":
            self.EXP = False
            print("除草捉虫经验已满！")

    def extractFlower(self, fid, fpotid, name, flower_name):
        data = {"data": {"friendId": fid, "potId": fpotid, "userId": self.sessionId}, "checkTime": self.time_stamp()}
        extractFlower = self.post_temple(extractFlower_url, self.JM.encode(str(data)))
        if extractFlower['code'] == '200':
            print(f"偷取{name}的{flower_name} 成功")
        elif extractFlower['msg'] == '请稍后再试':
            self.extractFlower(fid, fpotid, name, flower_name)
        else:
            print(f"偷取{name}的{flower_name}", extractFlower['msg'])

    def getSeedInfo(self):
        data = {"data": {"pageSize": "1", "pageNum": "300", "flowerName": "", "userId": self.sessionId},
                "checkTime": self.time_stamp()}
        getSeedInfo = self.post_temple(getSeedInfo_url, self.JM.encode(str(data)))['data']
        seedinfo = {}
        for i in getSeedInfo:
            seedinfo.update({str(i['uuid']): i['name']})
            print(i['uuid'], i['name'])
        print(seedinfo)


if __name__ == '__main__':
    start = time.time()
    HY = Garden()
    HY.login()
    HY.sign()
    HY.oneOperation()
    HY.oneHarvestFlower()
    # HY.flowerpot()
    # HY.sow(1, 1)
    HY.getMyFriends()
    HY.getFriendsPot()
    # HY.add_seed(buy_flower_id)
    print(f"共耗时{(time.time()-start):.2f}秒")
