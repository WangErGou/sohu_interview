# -*- coding:utf-8 -*-

import logging

from django.test import TestCase

from wxgz.utils import request_user_info_by_code_asy

logger = logging.getLogger(__name__)


class TestRequest(TestCase):

    def setUp(self):
        self.code = '041a45d289ea1f6d33de9ee01f584cei'

    def test_user_info(self):
        user_info = request_user_info_by_code_asy(self.code)
        self.assertTrue(user_info)
