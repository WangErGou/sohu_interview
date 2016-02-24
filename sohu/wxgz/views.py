# -*- coding:utf-8 -*-

from django.http import HttpResponse


def deal_server_verification(request):
    '''
    处理微信的服务器验证
    '''
    return HttpResponse('处理微信的服务器验证')


def deal_user_authorization(request):
    '''
    处理用户授权
    '''
    return HttpResponse('处理用户授权')


def get_self_info(request):
    '''
    获取用户自己的用户信息
    '''
    return HttpResponse('获取用户自己的用户信息')
