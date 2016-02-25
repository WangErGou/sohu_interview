# -*- coding: utf-8 -*-

from django.db import models


class User(models.Model):
    # 基本信息
    openid = models.CharField(max_length=128)
    nickname = models.CharField(max_length=256)
    SEX_ENUM = (
        (1, '男'),
        (2, '女'),
        (0, '未知')
    )
    sex = models.IntegerField(choices=SEX_ENUM, default=0)
    city = models.CharField(max_length=64)
    province = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    headimgurl = models.CharField(max_length=512)

    # refersh_token
    refresh_token = models.CharField(max_length=128)

    class Meta:
        db_table = 'weixin_user'

    def __unicode__(self):
        return u'{id}-{name}'.format(id=self.openid, name=self.nickname)
