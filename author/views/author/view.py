import json

from django.shortcuts import render
from django.http import HttpResponse

from author.views.author.authorization_view import Author
from lib.visualization.ColorPrint import color_format


def to_login(request):
    return render(request, 'author/toLogin.html')


def login(request):
    """
    登陆页
    :param request: 直接的登陆请求
    :return:
    """
    return render(request, 'author/login.html')


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
