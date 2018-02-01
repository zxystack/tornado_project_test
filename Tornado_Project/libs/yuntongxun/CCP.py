# coding:utf-8

from CCPRestSDK import REST
import ConfigParser

_accountSid= '8aaf0708588b1d2301588b68ffa5005a'; 
#说明：主账号，登陆云通讯网站后，可在"控制台-应用"中看到开发者主账号ACCOUNT SID。

_accountToken= 'adaa2a6dfc1b44c3acea27838f254dc4'; 
#说明：主账号Token，登陆云通讯网站后，可在控制台-应用中看到开发者主账号AUTH TOKEN。

_appId='8aaf0708588b1d2301588b6901730061'; 
#请使用管理控制台首页的APPID或自己创建应用的APPID.

_serverIP='sandboxapp.cloopen.com';
#说明：请求地址，生产环境配置成app.cloopen.com。

_serverPort='8883'; 
#说明：请求端口 ，生产环境为8883.

_softVersion='2013-12-26'; #说明：REST API版本号保持不变。 

class _CCP(object):
    def __init__(self):
        self.rest = REST(_serverIP, _serverPort, _softVersion) 
        self.rest.setAccount(_accountSid, _accountToken) 
        self.rest.setAppId(_appId)

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        return self.rest.sendTemplateSMS(to, datas, tempId)

ccp = _CCP.instance()

if __name__ == '__main__':
    ccp.sendTemplateSMS('18611833452', ['1234', 5], 1)


# 单例模式
# 对于一个类而言，只有一个全局唯一的实例
# class A(object)

# obj = A()

# obj = A.instance()
# obj = A.instance()
# obj = A.instance()
# obj = A.instance()
