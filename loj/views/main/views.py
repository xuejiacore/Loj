import logging

from django.http.response import Http404
from django.shortcuts import render

from Personal import settings
from author.models import User
from author.views.author.author import authorize

IMAGE_UPLOAD_PATH = settings.IMAGE_UPLOAD_PATH

logger = logging.getLogger('app')


@authorize()
def main(request, whose):
    # 检查当前的请求博客所属的用户是否存在，如果不存在，抛出404
    if User.objects.filter(login_id=whose).count() == 0:
        raise Http404
    user = User.objects.filter(login_id__contains=whose).first()
    logger.debug('* 访问 ' + (user.real_name if user else whose) + ' 的博客首页')
    request.session['real_name'] = user.real_name if user else whose
    return render(request, 'loj/main.html', context={
        "host": whose,
    })


def welcome(request):
    return render(request, 'loj/index.html')


def tagdemo(request):
    return render(request, 'loj/tagdemo.html',
                  {'users': User.objects.all(),
                   'uldata': ['asd', 'asd', ['sdsff', 'fgfg'], 'sdsd']})


def nestable(request):
    return render(request, 'loj/nestable.html')


@authorize()
def menu_manager(request):
    return render(request, 'loj/resManage.html')


def developing(request, whose, description):
    return render(request, 'loj/developingPage.html', context={
        'description': description,
        'host': whose
    })
