# -*- coding:utf-8 -*-

import logging

from django.test import TestCase

from wxgz.utils import request_user_info_by_code_asy

logger = logging.getLogger(__name__)


class TestRequest(TestCase):

    def setUp(self):
        self.code = '001a02ffb681355d89a4f8f8fea0e2ej'

    def test_user_info(self):
        user_info = request_user_info_by_code_asy(self.code)
        self.assertTrue(user_info)
