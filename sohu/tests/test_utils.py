# -*- coding:utf-8 -*-

from django.test import TestCase

from wxgz.utils import verify_signature, save_user_info


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

    def test_save_user_info(self):
        user_info = {
            u'province': u'北京',
            u'openid': u'oPTEpsxn0gkqSrXLMkLVliH2j-hc',
            u'headimgurl': u'http://wx.qlogo.cn/mmopen/HdFibw88iaIdjcAMian80SqGKtXsoT6CKEYY5ibyUDibAxkLO5KFXudTicr2csZDdAENn5GwCEHNNV4lMib5SCVyo2H2vF7HVLic8eBY/0',
            u'language': u'zh_CN',
            u'city': u'',
            u'country': u'中国',
            u'sex': 1,
            u'privilege': [],
            u'nickname': u'王琰杰'
        }
        user = save_user_info(user_info)
        self.assertEqual(u'北京', user.province)
        self.assertEqual(u'oPTEpsxn0gkqSrXLMkLVliH2j-hc', user.openid)
        self.assertEqual(u'http://wx.qlogo.cn/mmopen/HdFibw88iaIdjcAMian80SqGKtXsoT6CKEYY5ibyUDibAxkLO5KFXudTicr2csZDdAENn5GwCEHNNV4lMib5SCVyo2H2vF7HVLic8eBY/0', user.headimgurl)
        self.assertEqual(u'中国', user.country)
        self.assertEqual(u'男', user.get_sex_display())
        self.assertEqual(u'王琰杰', user.nickname)

