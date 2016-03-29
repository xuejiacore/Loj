import json

from django.http import HttpResponse
from django.shortcuts import render

from author.views.author.author import authorize
from author.views.author.authorization_view import Author


def to_login(request):
    return render(request, 'author/toLogin.html')


def profile(request):
    return render(request, 'author/profile.html')


def demo_func(request):
    print("这是从预处理函数传入的", request)


@authorize()
def login(request):
    """
    登陆页
    :param request: 直接的登陆请求
    :return:
    """
    return render(request, 'author/login.html')


@authorize()
def author(request):
    """
    用户的登陆认证
    :param request:
    :return:
    """
    response_json = Author().login(request)
    if not response_json:
        return render(request, 'author/login.html')
    return HttpResponse(json.dumps(response_json), content_type="application/json")
