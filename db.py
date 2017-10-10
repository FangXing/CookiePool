from config import *
from errors import *
import redis,random

#操作RedisClient的基类
class RedisClient(object):

    def __init__(self,host,port,password):
        if password:
            self._db = redis.Redis(host=host, port=port,password=password)
        else:
            self._db = redis.Redis(host=host,port=port)
        self.domain = REDIS_DOMAIN
        self.name = REDIS_NAME

    def get(self,key):
        raise NotImplementedError

    def set(self,key,value):
        raise NotImplementedError

    def delete(self,key):
        raise NotImplementedError

    def flush(self):
        self._db.flushdb()

    #格式化key
    def resolve_key(self, key):
        return "{}:{}:{}".format(self.domain,self.name,key)

    #获取所有key
    def keys(self):
        return self._db.keys("{domain}:{name}:*".format(domain=self.domain,name=self.name))


#账户的Redis操作类
class AccountRedisClient(RedisClient):

    def __init__(self,host=REDIS_HOST_NAME,port=REDIS_HOST_PORT,password=REDIS_PWD,domain='account',name='default'):
        super().__init__(host,port,password)
        self.domain=domain
        self.name=name

    def get(self,key):
        try:
            value = self._db.get(self.resolve_key(key))
            if value:
                return value.decode('utf-8')
            else:
                return None
        except:
            raise GetAccountException

    def set(self,key,value):
        try:
            return self._db.set(self.resolve_key(key), value)
        except:
            raise SetAccountException

    def delete(self,key):
        try:
            self._db.delete(self.resolve_key(key))
        except:
            raise DeleteAccountException

    #获取所有账户，以dict形式返回
    def all(self):
        try:
            for key in self.keys():
                password = self._db.get(key).decode('utf-8')
                grp = key.decode('utf-8').split(':')
                username = grp[2]
                result = {
                    'username':username,
                    'password':password
                }
                yield  result
        except Exception as e:
            raise GetAllAccountException


class CookieRedisClient(RedisClient):

    def __init__(self,host=REDIS_HOST_NAME,port=REDIS_HOST_PORT,password=REDIS_PWD,domain='cookie',name='default'):
        super().__init__(host,port,password)
        self.domain=domain
        self.name=name

    def get(self, key):
        try:
            value = self._db.get(self.resolve_key(key))
            if value:
                return value.decode('utf-8')
            else:
                return None
        except Exception as e:
            raise GetCookieException

    def set(self, key, value):
        try:
            return self._db.set(self.resolve_key(key), value)
        except:
            raise SetCookieException

    def delete(self, key):
        try:
            self._db.delete(self.resolve_key(key))
        except:
            raise DeleteCookieException

    #返回所有cookie，以dict形式返回
    def all(self):
        try:
            for key in self.keys():
                cookie = self._db.get(key).decode('utf-8')
                grp = key.decode('utf-8').split(':')
                username = grp[2]
                result = {
                    'username': username,
                    'cookie': cookie
                }
                yield result
        except:
            raise GetAllCookieException

    #随机返回一个cookie
    def random(self):
        try:
            key =  random.choice(self.keys())
            return self._db.get(key)
        except:
            raise RandomCookieException

    def count(self):
        try:
            return len(self.keys())
        except:
            raise CountCookieException


# if __name__ == '__main__':

    # arc.set('fx','124')
    # arc.set('fxl', '1124')
    # print(arc.get('fx'))
    # arc.delete('fx')
    # print(list(arc.all()))

    # crc = CookieRedisClient()
    # crc.set('ccok1','2222')
    # crc.set('ccok2', '333')

    # print(crc.random())
    # crc.delete('ccok1')
    # print(crc.count())
    # print(list(crc.all()))

