import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render

from author.views.author.author import authorize
from author.models import User
from blog.forms import BlogPublishForm
from blog.models import Blog, BlogCategory
from lib.visualization.ColorPrint import color_format

logger = logging.getLogger('app')


def blog_outline(request, whose):
    return render(request, 'blog/outline.html')


def blog_category(request, whose):
    return render(request, 'blog/categories.html')


def blog_create_category(request, whose):
    response = {
        'error': 'success'
    }
    if request.is_ajax() and request.method == 'POST':
        # 查询当前创建的博客分类是否已经存在于数据库中，如果已经存在，提示用户分类已经存在，放弃入库
        current_user = User.objects.get(login_id=request.session['login_id'])
        try:
            category = request.POST['categoryName']
            count = BlogCategory.objects.filter(name=category, user=current_user).count()
            if count:
                response['error'] = 'failure'
                response['msg'] = '创建的分类已经存在'
            else:
                blog_category = BlogCategory()
                blog_category.name = category
                blog_category.user = current_user
                blog_category.save()
                blog_category = BlogCategory.objects.filter(name=category, user=current_user).first()
                response['category_id'] = blog_category.category_id
        except KeyError:
            response['error'] = 'failure'
            response['msg'] = '非法请求'
    else:
        response['error'] = 'failure'
        response['msg'] = '非法请求'
    return HttpResponse(json.dumps(response), content_type="application/json")


@authorize()
def blog_editor(request, whose):
    """
    博客编辑页面逻辑
    :param request: 请求
    :param whose: 博客的拥有者
    :return:
    """
    category = BlogCategory.objects.filter(user=User.objects.get(login_id=request.session['login_id']))
    print(category)
    return render(request, 'blog/blogEditor.html', {
        'blog_categories': category
    })


# 博客目录页每页显示的数量
CATALOG_COUNT_PER_PAGE = 5


def blog_catalog(request, whose, page):
    """
    博客目录显示
    :param request: 请求
    :param whose: 博客的拥有者
    :param page: 当前需要显示的页码
    :return:
    """
    # 第一页 0:5  5:10 n * page-1 ： n * page
    current_page = int(page)
    blog_list = Blog.objects.filter(user=User.objects.get(login_id=whose))
    catalog = blog_list.order_by('-top', '-publish_date')[
              CATALOG_COUNT_PER_PAGE * (current_page - 1):
              CATALOG_COUNT_PER_PAGE * current_page]
    request.session['host'] = whose

    # 页码总数
    page_size = int(round(blog_list.count() / CATALOG_COUNT_PER_PAGE))

    # 从当前页开始，向两边进行探测，如果没有超出最小值和最大值，那么就是界
    low_limit = current_page - 1 if current_page - 1 > 0 else 1
    low_limit = low_limit - 1 if low_limit - 1 > 0 else 1

    upper_limit = current_page + 1 if current_page + 1 <= page_size else page_size
    upper_limit = upper_limit + 1 if upper_limit + 1 <= page_size else page_size

    # 生成用于显示的页码
    pages = [page for page in range(low_limit, upper_limit + 1, 1)]
    return render(request, 'blog/blogCatalog.html', {
        'blog_list': catalog,
        'host': whose,
        'last_page': current_page - 1,
        'current_page': current_page,
        'next_page': current_page + 1,
        'page_list': pages,
        'page_size': page_size
    })


def blog_detail(request, whose, blog_id):
    """
    博客的详细内容
    :param request: 请求
    :param whose: 博客的拥有者
    :param blog_id: 博客的ID号
    :return:
    """
    blog = Blog.objects.get(blog_id=blog_id, user=User.objects.get(login_id=whose))
    blog.read_times += 1
    blog.save()
    return render(request, 'blog/blogDetail.html', {
        'blog': blog
    })


def blog_delete(request, whose, blog_id):
    """
    删除博客的操作
    :param request: 请求
    :param whose: 博客的拥有者
    :param blog_id: 博客的ID号
    :return:
    """
    response = {}
    try:
        result = Blog.objects.get(blog_id=blog_id).delete()
    except ObjectDoesNotExist:
        response['error'] = 'error'
    else:
        response['error'] = 'ok' if result[0] == 1 else 'error'
    return HttpResponse(json.dumps(response), content_type="application/json")


def blog_publish(request, whose):
    """
    发表博客
    前台使用的Ajax请求
    :param request:请求
    :param whose:当前请求用户的唯一标识
    :return:
    """
    if request.method == 'POST' and request.is_ajax():
        try:
            blog_title = request.POST['blogTitle']
            blog_content = request.POST['blogContent']
            category = request.POST['blogCategory']
        except KeyError:
            logger.debug('* 带非法参数请求，已经拒绝用户')
            raise Http404

        logger.debug('* BLOG TITLE:' + blog_title)
        logger.debug('* BLOG CONTENT:' + blog_content)
        logger.debug('* BLOG CATALOG:' + category)
        # 使用博文表单验证对表单的合法性做确认
        form = BlogPublishForm(request.POST)
        response = {}
        if form.is_valid():
            logger.debug('* 信息均已经填写完整，通过表单验证，写入数据库')
            # TODO:在这里对数据的内容进行入库操作

            publish_ip = request.META['REMOTE_ADDR']
            print(color_format("* 客户端的IP地址是：{}".format(publish_ip), fore='cyan'))
            user = User.objects.get(login_id=request.session['login_id'])
            blog = Blog()
            # 设值博文的标题
            blog.blog_title = blog_title
            # 设值博文发表的内容
            blog.blog_content = blog_content
            # 设置博文发表者的IP
            blog.publish_ip = publish_ip
            # 设置博文的分类
            blog.category = BlogCategory.objects.filter(user=user,
                                                        name='默认').first()
            blog.keywords = '测试关键字'
            blog.user_id = user.user_id
            blog.save()

            response['error'] = 'success'
            response['msg'] = '博客进入审核阶段，审核合法后发表'
        else:
            logger.debug('* 博客内容不完整')
            response['error'] = 'error'
            response['msg'] = '博客内容不完整'
        return HttpResponse(json.dumps(response), content_type='application/json')
    else:
        logger.debug('* 非法请求方式，已经拒绝用户')
        raise Http404
