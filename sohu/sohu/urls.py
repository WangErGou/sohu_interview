from django.conf.urls import include, url
from django.contrib import admin

from wxgz import views as wxgz_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^serviceVerification$', wxgz_views.deal_server_verification),
    url(r'^userAuthorization/$', wxgz_views.deal_user_authorization),
    url(r'^userInfo/$', wxgz_views.get_self_info, name='GetUserInfo'),
]
