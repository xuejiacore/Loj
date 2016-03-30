import collections

from Personal import settings
from lib.visualization.ColorPrint import color_format
from django.http import HttpResponseRedirect, HttpRequest
from django.core.urlresolvers import reverse

# 认证使用的配置文件
try:
    author_settings = settings.AUTHOR_SETTINGS
except AttributeError:
    author_settings = {
        # 是否启用调试模式
        "debug": False,
        # 默认的重定向地址
        "redirect": "unknown",
        # 不进行过滤的请求地址
        "ignore_req": [
            'login'
        ],
        # 如果请求下面的内容将会清楚存留的用户信息
        'clear_req': [
            'login'
        ]
    }


def authorize(*args, **kwargs):
    """
    认证登录装饰拦截
    对请求进行判断，是否是已经认证的用户，如果不是认证过的，那么将重定向到指定的重定向地址中
    :param args:
    :param kwargs:
        pre_func:预处理函数对象，在处理request认证之前执行
        post_func:预处理函数对象，在处理request认证之后执行
        tag:拦截标签
        express_and:附加的"与"条件表达式
        express_or:附加的"或"条件表达式
    :return:
    """

    def _decorate(view):
        def __decorate(*fn_args, **fn_kwargs):
            is_debug = kwargs.get("debug") if "debug" in kwargs else author_settings.get("debug")
            redirect_url = author_settings.get("redirect")

            tag = kwargs.get("tag")
            if is_debug:
                print(color_format("TAG: {}".format(tag), fore='cyan'))

            bool_and = kwargs.get("express_and")
            bool_or = kwargs.get("express_or")

            # ---------------------------------------------------------------------------------------------预处理开始
            # 根据参数中是否提供了预处理函数进行预处理程序的加载
            pre_deal = kwargs.get("pre_func")
            if pre_deal and isinstance(pre_deal, collections.Callable):
                del kwargs['pre_func']
                pre_result = pre_deal(*fn_args, **fn_kwargs)
                if is_debug:
                    print(color_format("The pre_result is: {}".format(pre_result)))

            # ---------------------------------------------------------------------------------------------检查放行请求
            request = fn_args[0] if isinstance(fn_args[0], HttpRequest) else fn_kwargs.get('req')
            if view.__name__ in author_settings['ignore_req'] or 'anonymous' in request.path:
                if is_debug:
                    print(color_format("不拦截的请求: {}".format(view.__name__), fore='cyan'))
                if view.__name__ in author_settings['clear_req'] or 'anonymous' in request.path:
                    if 'login_id' in request.session:
                        del request.session['login_id']
                    if 'visit_role' in request.session:
                        del request.session['visit_role']
                    print("清除用户的登录信息")
                ret = view(*fn_args, **fn_kwargs)

                __post_deal(fn_args, fn_kwargs, is_debug)
                return ret

            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            if is_debug:
                print(color_format("当前请求的view是：{}".format(view.__name__), fore='cyan'))
            # HttpResponseRedirect(reverse(author_settings['redirect']))
            if not request:
                if is_debug:
                    print(color_format("You must provide the request instance!", mode='bold', fore='cyan'))
                raise KeyError
            session = request.session

            # 检查session中是否有已经登陆的用户的信息
            role = session['visit_role'] if 'visit_role' in session else 'anonymous'
            if is_debug:
                print(color_format("访问身份：{}".format(role), fore='cyan'))

            if role == 'anonymous':
                # TODO:匿名用户
                if is_debug:
                    print(color_format("是匿名用户在访问，并且加了认证装饰器，拒绝该请求:{}".format(view.__name__), fore='cyan'))
                    # 记录用户的请求意图，用于登陆后进行直接的跳转
                    request.session['request_path'] = request.path
                    print(request.session['request_path'])
                    ret = HttpResponseRedirect(reverse(author_settings['redirect']))
                    __post_deal(fn_args, fn_kwargs, is_debug)
                    return ret
            elif role == 'user' and 'login_id' in session:
                # TODO:登录用户
                if 'whose' in fn_kwargs and session['login_id'] != fn_kwargs['whose']:
                    return HttpResponseRedirect(reverse(author_settings['redirect']))
                print(color_format("当前登录用户的id是：{}".format(session['login_id']), fore='cyan'))

            print("-----------------------------------------------------------------")
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理
            # ---------------------------------------------------------------------------------------------认证有效性的核心处理

            # ---------------------------------------------------------------------------------------------后处理开始
            ret = view(*fn_args, **fn_kwargs)

            # 根据参数中是否提供了后处理函数进行后处理程序的加载
            post_deal = fn_kwargs.get("post_func")
            if post_deal and isinstance(post_deal, collections.Callable):
                post_result = post_deal(*fn_args, **fn_kwargs)
                if is_debug:
                    print(color_format("The post_result is: {}".format(post_result)))

            # 返回原函数的返回结果
            return ret

        def __post_deal(fn_args, fn_kwargs, is_debug):
            post_deal = fn_kwargs.get("post_func")
            if post_deal and isinstance(post_deal, collections.Callable):
                post_result = post_deal(*fn_args, **fn_kwargs)
                if is_debug:
                    print(color_format("后处理程序的执行结果是: {}".format(post_result)))

        return __decorate

    return _decorate
