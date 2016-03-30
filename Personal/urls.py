"""Personal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from loj.views.main.views import welcome, main, tagdemo, nestable, menu_manager

# 整站的URL配置
urlpatterns = [
    # ##################################################################################################################
    # 博客入口
    # ##################################################################################################################
    #
    # 用户的博客入口必须满足格式：/<username>/blog/
    url(r'^(?P<whose>\w+)/blog/', include('blog.urls')),

    # ##################################################################################################################
    # 用户认证入口
    # ##################################################################################################################
    #
    # 用户体系的认证相关url配置
    url(r'^author/', include('author.urls')),

    # ##################################################################################################################
    # 框架页面
    # ##################################################################################################################
    #
    # 使用用户登录的方式进入主页面
    url(r'^(?P<whose>\w+)/main/$', main, name="main"),
    # 使用匿名用户进入主页面
    url(r'^(?P<whose>\w+)/main/anonymous/$', main, name='anonymous'),
    # TODO:管理员页面，部署时可以考虑是否对该页面进行安全限制，如IP鉴权或者是用户鉴权的方式等
    url(r'^admin/', admin.site.urls),
    # 欢迎页面
    url(r'^welcome/$', welcome, name='welcome'),
    url(r'^$', welcome),
    # 主页面

    # 测试页面
    url(r'^tagdemo/$', tagdemo, name='tagdemo'),
    url(r'^nestable/$', nestable, name='nestable'),
    url(r'^resManager/$', menu_manager, name='menuManager')
]
