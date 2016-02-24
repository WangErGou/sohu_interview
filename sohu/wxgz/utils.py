# -*- coding:utf-8 -*-

import logging
import hashlib
from functools import wraps

logger = logging.getLogger(__name__)


# ----------------------------------------------
#       Http Request
# ----------------------------------------------
def request_access_token(code):
    '''
    根据用户授权后返回的 code 来请求 access_token
    '''
    pass


def request_user_info_asy(openid, access_token, lang='zh_CN'):
    '''
    根据用户 id 和 access_token 来请求用户的信息
    '''
    pass


def request_user_info_by_code_asy(code, lang='zh_CN'):
    '''
    根据用户授权后返回的 code 来获取用户信息
    '''
    pass


# ----------------------------------------------
#       Decorator
# ----------------------------------------------
def authorized(func):
    '''
    确保用户已授权，否则重定向到授权页面
    '''
    pass


def log_params(func):
    @wraps(func)
    def _wrapped_func(request, *args, **kwargs):
        logger.debug('URI: {0}\n'.format(request.path))
        logger.debug('GET Params:\n{0}\n'.format(
            ' '.join('{k}: {v}'.format(k=k, v=v) for k, v in request.GET.items())))
        logger.debug('POST Params:\n{0}\n'.format(
            ' '.join('{k}: {v}'.format(k=k, v=v) for k, v in request.GET.items())))
        return func(request, *args, **kwargs)
    return _wrapped_func


# ----------------------------------------------
#       Utils
# ----------------------------------------------
def verify_signature(token, timestamp, nonce, signature):
    '''
    验证签名的有效性

    计算签名的方法：
        1. 对 token，timestamp，nonce 三个字符串按字典序排序后拼接在一起
        #. 计算拼接后的字符串的 sha1 值（十六进制）
    '''
    expected_signature = hashlib.sha1(
        ''.join(sorted([token, timestamp, nonce]))).hexdigest()
    return expected_signature == signature


def get_user_info(code):
    pass
