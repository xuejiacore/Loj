import logging

from django.http.response import Http404
from django.shortcuts import render
from django.template import Context, Template

from Personal import settings
from author.models import User

IMAGE_UPLOAD_PATH = settings.IMAGE_UPLOAD_PATH

logger = logging.getLogger('app')


def main(request, whose):
    user = User.objects.filter(login_id__contains=whose).first()
    logger.debug('* 访问 ' + (user.real_name if user else whose) + ' 的博客首页')
    # 检查当前的请求博客所属的用户是否存在，如果不存在，抛出404
    if User.objects.filter(login_id=whose).count() == 0:
        raise Http404
    if 'host' not in request.session:
        request.session['host'] = whose
    return render(request, 'loj/main.html')


def welcome(request):
    return render(request, 'loj/index.html')


def tagdemo(request):
    return render(request, 'loj/tagdemo.html',
                  {'users': User.objects.all(),
                   'uldata': ['asd', 'asd', ['sdsff', 'fgfg'], 'sdsd']})
