#定义系统里的异常

class CookiePoolException(Exception):
    def __init__(self,err='cookiepool异常'):
        super().__init__(err)

class GetAccountException(CookiePoolException):
    def __init__(self, err='获取account异常'):
        super().__init__(err)

class SetAccountException(CookiePoolException):
    def __init__(self, err='设置account异常'):
        CookiePoolException.__init__(err)

class DeleteAccountException(CookiePoolException):
    def __init__(self, err='删除account异常'):
        super().__init__(err)

class GetAllAccountException(CookiePoolException):
    def __init__(self, err='获取所有account异常'):
        super().__init__(err)

class GetCookieException(CookiePoolException):
    def __init__(self, err='获取cookie异常'):
        super().__init__(err)

class SetCookieException(CookiePoolException):
    def __init__(self, err='设置cookie异常'):
        super().__init__(err)

class DeleteCookieException(CookiePoolException):
    def __init__(self, err='删除cookie异常'):
        super().__init__( err)

class GetAllCookieException(CookiePoolException):
    def __init__(self, err='获取所有cookie异常'):
        super().__init__( err)

class RandomCookieException(CookiePoolException):
    def __init__(self, err='获取随机cookie异常'):
        super().__init__(err)


class CountCookieException(CookiePoolException):
    def __init__(self, err='统计cookie异常'):
        super().__init__(err)