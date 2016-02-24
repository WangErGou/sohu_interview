# -*- coding:utf-8 -*-

from django.http import HttpResponse
from django.conf import settings

from wxgz.utils import (
    get_user_info, authorized, verify_signature, request_user_info_by_code_asy
)


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
    request.session['user_code'] = code
    # 根据 code 请求用户信息
    request_user_info_by_code_asy(code)
    return HttpResponse('处理用户授权')


@authorized
def get_self_info(request):
    '''
    获取用户自己的用户信息
    '''
    code = request.session['user_code']
    user_info = get_user_info(code)
    return HttpResponse('获取用户自己的用户信息')
