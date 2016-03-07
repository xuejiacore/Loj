from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404

from Personal import settings
from author.models import User
from lib.visualization.ColorPrint import color_format


class QtsAuthenticationMiddleware(object):
    """
    认证中间件
    """

    def process_request(self, request):
        """
        在请求发送置后，确定了请求视图之前触发
        :param request:
        :return:
        """
        return None

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Request 的预处理函数
        过滤请求，判断用户是否已经登陆过了，如果已经登陆，那么对用户的请求进行放行，否则将用户引导到登陆界面进行登陆后在
        进行其他的操作
        :param request:用户的请求
        :return:
        """
        # 排除login以及author两个请求
        login_path = reverse('author:login')
        author_path = reverse('author:author')
        print(color_format("请求参数：{}".format(view_kwargs), fore='cyan'))

        if 'whose' in view_kwargs and not User.objects.filter(login_id=view_kwargs.get('whose')).count():
            # 如果用户尝试请求不存在的用户博客，将会抛出404错误
            raise Http404

        if self.not_contain_paths(settings.AUTHOR_EXCLUDE_PATH, request):

            if login_path not in request.get_raw_uri() \
                    and author_path not in request.get_raw_uri():
                # 用户没有登陆，并且请求的不是登陆页的时候，需要对用户请求的路径进行缓存，用于当用户登陆成功后进行自动的跳转
                if 'login_id' not in request.session:
                    # 记录用户的请求意图，用于登陆后进行直接的跳转
                    request.session['request_path'] = request.path
                    request.session['302_request'] = request.path
                    print(color_format("request path = {}".format(request.path), mode='bold', fore='cyan'))
                    return HttpResponseRedirect(reverse('author:login'))
                if 'whose' in view_kwargs \
                        and 'host' in request.session \
                        and view_kwargs.get('whose') != request.session['host']:
                    request.session['host'] = view_kwargs.get('whose')
                    self.clear_session(request)
                    return HttpResponseRedirect(reverse('author:login'))
            else:
                # TODO:如果再次进入认证界面，如果session依然有效，清除session中的内容，用户需要重新进行登陆
                if "login_id" in request.session:
                    del request.session['login_id']
                if "password" in request.session:
                    del request.session['password']

        else:
            # 使用匿名用户进行网页浏览
            if 'anonymous' in request.path:
                if "login_id" in request.session:
                    del request.session['login_id']
                if "password" in request.session:
                    del request.session['password']
                if 'whose' in view_kwargs:
                    request.session['host'] = view_kwargs.get('whose')
                request.session['visit_role'] = 'anonymous'
                print("以游客的方式进行访问")
        return None

    @staticmethod
    def not_contain_paths(paths, request):
        """
        排除不过滤的请求
        :param paths: 需要排除的关键路径
        :param request: 请求
        :return:
        """
        path = request.path
        if '/' == path:
            return False
        for p in paths:
            if p in path:
                return False
        return True

    @staticmethod
    def clear_session(request):
        if 'username' in request.session:
            del request.session['username']
        if 'visit_role' in request.session:
            del request.session['visit_role']
