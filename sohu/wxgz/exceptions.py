# -*- coding:utf-8 -*-


class WXRequestException(Exception):
    '''
    记录向微信请求数据时返回结果为错误的情况
    '''

    def __init__(self, uri, wx_err):
        super(WXRequestException, self).__init__(wx_err)
        self.uri = uri
        self.wx_err = wx_err
