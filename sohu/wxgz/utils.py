# -*- coding:utf-8 -*-


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


# ----------------------------------------------
#       Utils
# ----------------------------------------------
def verify_signature(token, timestamp, nonce, signature):
    '''
    验证签名的有效性
    '''
    return True


def get_user_info(code):
    pass
