# -*- coding:utf-8 -*-

import logging
import hashlib
from functools import wraps

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import redirect

from wxgz.models import User

logger = logging.getLogger(__name__)


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
            logger.debug('authorized hello')
            return redirect(settings.ACCESS_SERVICE_URI)
    return _wrapped_func


# just for debug
def log_params(func):
    '''
    接口调试。
    记录请求的 URI，GET，POST 参数
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
    user = User.objects.get(openid=openid)
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
    logger.error('数据库错误: {0}'.format(e))
