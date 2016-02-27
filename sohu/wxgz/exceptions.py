# -*- coding:utf-8 -*-


from django.utils.datastructures import MultiValueDictKeyError
from django.core.exceptions import ObjectDoesNotExist


class WXRequestException(Exception):
    '''
    记录向微信请求数据时返回结果为错误的情况
    '''

    def __init__(self, uri, wx_err):
        super(WXRequestException, self).__init__(wx_err)
        self.uri = uri
        self.wx_err = wx_err


UserDoesNotExist = ObjectDoesNotExist


# 接口调用错误
class ParamError(Exception):
    '''
    参数错误
    '''
    pass


# 参数缺失
ParamMiss = MultiValueDictKeyError


# 未考虑的服务端错误
class ServerException(Exception):
    '''
    服务端错误
    '''
    pass
