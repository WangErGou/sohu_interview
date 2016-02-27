# -*- coding:utf-8 -*-

import logging
import traceback

from django.shortcuts import render_to_response
from django.template import RequestContext

from wxgz.exceptions import ParamError, ParamMiss

logger = logging.getLogger(__name__)


class ViewExceptionMiddleware(object):

    def process_exception(self, request, exception):
        '''
        根据异常的类型，选择对应的处理函数
        '''
        if isinstance(exception, ParamError):
            return self.process_param_error(request, exception)
        elif isinstance(exception, ParamMiss):
            return self.process_param_miss(request, exception)
        else:
            return self.process_server_exception(request, exception)

    error_template = 'info.html'

    ParamErrorErr = 0
    ParamErrorMsg = '参数错误'

    ParamMissErr = 2
    ParamMissMsg = '参数缺失'

    ServerExceptionErr = 3
    ServerExceptionMsg = '服务端错误'

    def process_param_error(self, request, exception):
        '''
        处理参数错误
        '''
        logger.info('参数错误: {ip}\n{param}'.format(
            ip=request.get_host(), param=self.format_param(request)))
        return render_to_response(
            self.error_template, {'summary': '参数错误'},
            context_instance=RequestContext(request))

    def process_param_miss(self, request, exception):
        '''
        处理参数缺失
        '''
        logger.info('参数错误: {ip}\n{param}'.format(
            ip=request.get_host(), param=self.format_param(request)))
        return render_to_response(
            self.error_template, {'summary': '参数缺失'},
            context_instance=RequestContext(request))

    def process_server_exception(self, request, exception):
        '''
        处理服务端错误
        '''
        logger.error(traceback.format_exc())
        return render_to_response(
            self.error_template,
            {
                'summary': '服务端错误',
                'detail': '请联系 g-sec-dev@360.cn',
            },
            context_instance=RequestContext(request))

    def format_param(self, request):
        return 'GET: {get}\nPOST: {post}\nCOOKIES: {cookies}'.format(
            get=request.GET, post=request.POST, cookies=request.COOKIES)
