# -*- coding:utf-8 -*-

import logging
import hashlib
import json
from functools import wraps

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from wxgz.models import User
from wxgz.exceptions import WXRequestException

logger = logging.getLogger(__name__)


# ----------------------------------------------
#       Request from weixin
# ----------------------------------------------
def query_from_wx(uri, params={}, method='get'):
    r = getattr(requests, method)(uri, params=params, verify=False)
    data = json.loads(r.content)
    if 'errcode' in data:
        raise WXRequestException(r.url, data)
    return data


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
    data = query_from_wx(settings.ACCESS_TOKEN_URI, params)
    logger.debug('user authorization: {0}'.format(data))    # debug
    openid = data['openid']
    access_token = data['access_token']
    expires_in = data['expires_in']
    refresh_token = data['refresh_token']

    save_token(openid, access_token, expires_in, refresh_token)
    # redis: code --> openid
    cache.set(code, openid)
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
    user_info = query_from_wx(settings.USER_INFO_URI, params)
    logger.debug('user info: {0}'.format(user_info))    # debug
    save_user_info(user_info)
    return user_info


def save_token(openid, access_token, expires, refresh_token):
    '''
    保存 access_token 到 cache 和 refresh_token 到数据库
    '''
    # redis: openid --> access_token, expires_in
    cache.set(openid, (access_token, expires), timeout=expires)
    # MySQL: openid --> refresh_token
    try:
        user = User.objects.get_or_create(openid=openid)
        user.refresh_token = refresh_token
        user.save()
    except Exception as e:
        log_db_exception(e)


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


def request_user_info_by_code_asy(code, lang='zh_CN'):
    '''
    根据用户授权后返回的 code 来获取用户信息
    '''
    try:
        openid, access_token = request_access_token(code)
        user_info = request_user_info(openid, access_token)
    except WXRequestException as e:
        logger.info('从微信请求数据失败。URI: {uri}, err: {err}'.format(
            uri=e.uri, err=e.wx_err))
        return None
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
    openid = cache.get(code)
    try:
        user = User.objects.get(openid=openid)
    except ObjectDoesNotExist:
        return None
    return package_user_info(user)


def package_user_info(user):
    '''
    将 User 封装成 dict
    '''
    return {
        'openid': user.openid,
        'nickname': user.nickname,
        'sex': user.get_sex_display(),
        'city': user.city,
        'province': user.province,
        'country': user.country,
        'headimgurl': user.headimgurl
    }


def log_db_exception(e):
    logger.error('数据库错误: {e}'.format(e))
