from django.core.urlresolvers import reverse
import logging

from author.models import User

logging = logging.getLogger('app')


class Author(object):
    def __init__(self):
        self.username = ''
        self.password = ''

    def login(self, request):
        """
        验证用户输入的用户名以及密码是否正确
        :param request: 用户的请求，携带用户名以及用户填写的密码
        :return: 返回打包完成的Json数据格式
        """
        if request.is_ajax() and request.method == "POST":
            self.username = request.POST["username"]
            self.password = request.POST["password"]
            # 准备响应Json内容
            response = {}

            if self.is_user_exist(self.username):
                correct_user = self.validate_user(self.username, self.password)
                if correct_user:
                    response["status"] = "OK"
                    try:
                        response['req_target'] = request.session['request_path']
                        del request.session['request_path']
                    except KeyError:
                        response['req_target'] = reverse("main", args=[self.username])
                        logging.debug('没有捕获 req_target = '.format(response['req_target']))

                    request.session['login_id'] = correct_user.login_id
                    request.session['real_name'] = correct_user.real_name
                    request.session['visit_role'] = 'user'
                    request.session['is_admin'] = False if self.username != 'root' else True
                    request.session['host'] = self.username
                    target = response['req_target']
                    tmp = target.split(sep='/')
                    tmp[1] = self.username
                    response['req_target'] = '/'.join(tmp)
                else:
                    response["status"] = "FAILURE"
                    response["errorMsg"] = "您输入的密码与用户名不匹配，请重试 :)"
            else:
                response["errorMsg"] = "您输入的用户名不存在，请重试 :)"
            return response

    @staticmethod
    def is_user_exist(username):
        return User.objects.filter(login_id=username).count()

    @staticmethod
    def validate_user(username, password):
        return User.objects.filter(login_id=username, password=password).first()
