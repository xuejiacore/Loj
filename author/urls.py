from django.conf.urls import url

from author.views.author.view import author, login, profile

app_name = 'author'

urlpatterns = [
    # 认证处理
    url(r'^author/$', author, name="author"),
    # 登陆页
    url(r'^login/$', login, name="login"),
    # 用户简介编辑页
    url(r'^profile/$', profile, name='profile')
]
