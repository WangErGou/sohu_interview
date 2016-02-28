# -*- coding:utf-8 -*-
from __future__ import absolute_import

import logging
import json

import requests
from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from wxgz.models import User
from wxgz.utils import log_db_exception
from wxgz.exceptions import WXRequestException

logger = logging.getLogger(__name__)


# ----------------------------------------------
#       Request from weixin
# ----------------------------------------------
def query_from_wx(uri, params={}, method='get'):
    '''
    从微信服务器请求数据。

    当网络出错或微信服务器返回错误时，都抛出异常
    '''
    try:
        r = getattr(requests, method)(uri, params=params, verify=False)
    except requests.exceptions.RequestException as e:
        logger.warning(e)
        raise WXRequestException(uri, 'requests异常')
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
        user, _ = User.objects.get_or_create(openid=openid)
        user.refresh_token = refresh_token
        user.save()
    except Exception as e:
        log_db_exception(e)


def save_user_info(user_info):
    '''
    将微信返回的用户信息保存到数据库中
    '''
    openid = user_info['openid']
    # get or create user
    user, _ = User.objects.get_or_create(openid=openid)
    # update data
    user.nickname = user_info['nickname']
    user.sex = user_info['sex']
    user.city = user_info['city']
    user.province = user_info['province']
    user.country = user_info['country']
    user.headimgurl = user_info['headimgurl']
    user.save()
    return user


@shared_task
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
    logger.debug('request_user_unfo: {user_info}'.format(user_info=user_info))  # debug
    return user_info
