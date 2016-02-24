# -*- coding:utf-8 -*-

from django.test import TestCase

from wxgz.utils import verify_signature


class TestUtils(TestCase):
    def test_verify_signature(self):
        token = 'Token123456'
        nonce = '794675585'
        timestamp = '1456335851'
        expected_signature = 'fe4155e4d9f1f19c4829f118148e8832858b9829'

        self.assertTrue(verify_signature(
            token, timestamp, nonce, expected_signature))
        self.assertFalse(verify_signature(
            token, timestamp, nonce, 'error'))
