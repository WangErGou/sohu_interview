# -*- coding:utf-8 -*-

import logging
import hashlib
import json
from functools import wraps

import requests
from django.conf import settings
from django.core.cache import cache

from wxgz.models import User

logger = logging.getLogger(__name__)


# ----------------------------------------------
#       Http Request
# ----------------------------------------------
def request_access_token(code):
    '''
    根据用户授权后返回的 code 来请求 access_token
    '''
    params = {
        'appid': settings.APPID,
        'secret': settings.APP_SECERT,
        'code': code,
        'grant_type': 'authorization_code',
    }
    r = requests.get(settings.ACCESS_TOKEN_URL, params=params, verify=False)
    data = r.json()
    if 'errcode' in data:
        # logging err
        return None
    # redis: openid --> access_token, expires_in
    openid = data['openid']
    access_token = data['access_token']
    expires_in = data['expires_in']
    assert isinstance(expires_in, int), type(expires_in)
    cache.set(openid, (access_token, expires_in), timeout=expires_in)
    # MySQL: openid --> refresh_token
    refresh_token = data['refresh_token']
    try:
        User(openid=openid, refresh_token=refresh_token).save()
    except Exception:
        # TODO: logging exception
        pass
    return openid, access_token


def request_user_info(openid, access_token, lang='zh_CN'):
    '''
    根据用户 id 和 access_token 来请求用户的信息
    '''
    params = {
        'access_token': access_token,
        'openid': openid,
        'lang': lang,
    }
    r = requests.get(settings.USER_INFO_URL, params=params, verify=False)
    user_info = json.loads(r.content)
    if 'errcode' in user_info:
        # TODO logging err
        return None
    return user_info


def request_user_info_by_code_asy(code, lang='zh_CN'):
    '''
    根据用户授权后返回的 code 来获取用户信息
    '''
    openid, access_token = request_access_token(code)
    user_info = request_user_info(openid, access_token)
    return user_info


# ----------------------------------------------
#       Decorator
# ----------------------------------------------
def authorized(func):
    '''
    确保用户已授权，否则重定向到授权页面
    '''
    @wraps(func)
    def _wrapped_func(request, *args, **kwargs):
        if 'user_code' in request.session:
            return func(request, *args, **kwargs)
        else:
            # 重定向到授权页面
            # TODO 怎么引导用户到授权页面，特别是用户首次进入时
            pass
    return _wrapped_func


def log_params(func):
    '''
    调试接口用，记录请求的 URI，GET，POST 参数
    '''
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


def save_user_info(user_info):
    '''
    将微信返回的用户信息保存到数据库中
    '''
    openid = user_info['openid']

    user, _ = User.objects.get_or_create(openid=openid)
    user.nickname = user_info['nickname']
    user.sex = user_info['sex']
    user.city = user_info['city']
    user.province = user_info['province']
    user.country = user_info['country']
    user.headimgurl = user_info['headimgurl']

    user.save()
    return user
