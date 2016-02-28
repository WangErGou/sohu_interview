==============
手机搜狐机试题
==============

本项目旨在完成手机搜狐提供的机试题。

题目描述
========

请实现 `微信公众平台 <https://mp.weixin.qq.com/>`_
的 `网页授权获取用户基本信息 <https://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html>`_
功能，要求：

    1. 授权后展示用户的详细信息
    #. 提供 github 提交历史
    #. 公众号的二维码，测试 URL

功能
====

实现的功能如下：

    1. 获取用户授权，并在回调中异步查询用户信息
    #. 提供接口用于展示用户自己的信息
    #. **（未实现）** 主动刷新 `access_token`

使用
====

1. 微信扫描二维码，关注测试公众号

.. image:: doc_image/92721b212421b73adb8a643aa51ae08d.jpg
    :align: center

2. 在微信中点击下面的链接，同意授权后，点击链接获取用户信息

`https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxb810fba238400a9f&redirect_uri=http%3A%2F%2F123.57.235.88%2FuserAuthorization%2F&response_type=code&scope=snsapi_userinfo&state=state#wechat_redirect
<https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxb810fba238400a9f&redirect_uri=http%3A%2F%2F123.57.235.88%2FuserAuthorization%2F&response_type=code&scope=snsapi_userinfo&state=state#wechat_redirect>`_

PS: 微信可能会弹出如下提示，可能需要多点几次才会弹出实际页面。

.. image:: doc_image/b91a6e424013456729786aaa09ec4f35.jpg
    :align: center
