# -*- coding:utf-8 -*-

import logging

from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from wxgz.utils import (
    get_user_info, verify_signature, request_user_info_by_code_asy,
    log_params, authorized,
)


logger = logging.getLogger(__name__)
TOKEN = settings.TOKEN


def deal_server_verification(request):
    '''
    处理微信的服务器验证
    '''
    signature = request.GET['signature']
    timestamp = request.GET['timestamp']
    nonce = request.GET['nonce']
    echostr = request.GET['echostr']
    if verify_signature(TOKEN, timestamp, nonce, signature):
        return HttpResponse(echostr)
    return HttpResponse('禁止访问')


def deal_user_authorization(request):
    '''
    处理用户授权
    '''
    code = request.GET['code']
    logger.debug('receive code: {code}'.format(code=code))  # debug
    request.session['user_code'] = code
    # 根据 code 请求用户信息
    request_user_info_by_code_asy(code)
    return render_to_response(
        'magic.html', {'uri': reverse('GetUserInfo')},
        context_instance=RequestContext(request))


@authorized
def get_self_info(request):
    '''
    获取用户自己的用户信息
    '''
    code = request.session['user_code']
    user_info = get_user_info(code)
    logger.debug(user_info) # debug
    if user_info is None:
        return render_to_response(
            'user_info.html', {'fail': True},
            context_instance=RequestContext(request))
    return render_to_response(
        'user_info.html', user_info,
        context_instance=RequestContext(request))
