from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter('append')
def append(values):
    return mark_safe("<h4><font color='red'>用户的姓名是：" + values + "</font></h4>")


@register.simple_tag(name='tagdemo')
def tagdemo(str):
    return '测试标签' + ' | ' + str
