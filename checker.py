import requests,json
from db import AccountRedisClient,CookieRedisClient
from bs4 import BeautifulSoup

class CookieChecker(object):
    def __init__(self,name='default'):
        self.name = name
        self._account_db = AccountRedisClient(name=self.name)
        self._cookie_db = CookieRedisClient(name=self.name)


    def check(self,account,cookies):
        raise NotImplementedError

    def run(self):
        accounts = self._account_db.all()
        for account  in accounts:
            username = account.get('username')
            cookies = self._cookie_db.get(username)
            if cookies and not self.check(account,cookies):
                # print('invalid cookie', account.get('username'))
                # self._cookie_db.delete(username)
                pass



class WeiboCookieChecker(CookieChecker):
    def __init__(self,name='weibo'):
        super().__init__(name)

    def check(self, account, cookies):
        test_url = 'http://weibo.cn/'

        cookies = json.loads(cookies)
        response = requests.get(test_url,cookies=cookies)
        try:
            if response.status_code == 200:
                bs = BeautifulSoup(response.text,'lxml')
                title = bs.title.string
                if title == '我的首页':
                   
                    print('valid cookie,'+account.get('username'))
                    return True
                else:
                    print('invalid cookie',account.get('username'))
            else:
                print('invalid status',response.status_code)
                print('invalid cookie', account.get('username'))
        except ConnectionError as e:
            print('测试cookie异常'+ e.args)


if __name__ == '__main__':
    wcc = WeiboCookieChecker()
    wcc.run()