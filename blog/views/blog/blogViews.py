import json
import logging

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.shortcuts import render
from math import ceil

from author.views.author.author import authorize
from author.models import User
from blog.forms import BlogPublishForm
from blog.models import Blog, BlogCategory
from lib.visualization.ColorPrint import color_format

logger = logging.getLogger('app')


def blog_outline(request, whose):
    # 第一页 0:5  5:10 n * page-1 ： n * page
    user = User.objects.get(login_id=whose)
    all_blog = Blog.objects.filter(user=user)
    categories = BlogCategory.objects.filter(user=user).order_by('-level', 'create_date')

    # 获得博客分类对应的博客数量
    blog_category_count = [{
                               'category_id': category.category_id,
                               'name': category.name,
                               'count': category.blog_category.count()
                           } for category in categories]

    default_bcc_count = 0
    for bcc in blog_category_count:
        if bcc['name'] == '默认分类':
            default_bcc_count = bcc['count']
            break

    return render(request, 'blog/outline.html', context={
        'blog_list': all_blog.order_by('-top', '-star', '-publish_date', '-blog_id')[0:8],
        'categories': blog_category_count,
        'host': whose,
        'blog_count': all_blog.count(),
        'default_count': default_bcc_count
    })


@authorize()
def blog_create_category(request, whose):
    response = {
        'error': 'success'
    }
    if request.is_ajax() and request.method == 'POST':
        # 查询当前创建的博客分类是否已经存在于数据库中，如果已经存在，提示用户分类已经存在，放弃入库
        current_user = User.objects.get(login_id=request.session['login_id'])
        try:
            category_name = request.POST['categoryName']
            if category_name:
                count = BlogCategory.objects.filter(name=category_name, user=current_user).count()
                if count:
                    response['error'] = 'failure'
                    response['msg'] = '创建的分类已经存在'
                else:
                    category = BlogCategory()
                    category.name = category_name
                    category.user = current_user
                    category.save()
                    category = BlogCategory.objects.filter(name=category_name, user=current_user).first()
                    response['category_id'] = category.category_id
            else:
                response['error'] = 'failure'
                response['msg'] = '分类名称不允许为空'
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
    category = BlogCategory.objects.filter(user=User.objects.get(login_id=request.session['login_id'])).order_by(
            '-level', 'create_date')
    print(category)
    return render(request, 'blog/blogEditor.html', {
        'blog_categories': category,
        'host': whose
    })


# 博客目录页每页显示的数量
CATALOG_COUNT_PER_PAGE = 5


def blog_catalog(request, whose, page, category_name):
    """
    博客目录显示
    :param category_name: 博客的分类名称
    :param request: 请求
    :param whose: 博客的拥有者
    :param page: 当前需要显示的页码
    :return:
    """
    # 第一页 0:5  5:10 n * page-1 ： n * page
    current_page = int(page)
    user = User.objects.get(login_id=whose)
    category_list = BlogCategory.objects.filter(user=user).order_by('-create_date', '-level')
    all_blog = Blog.objects.filter(user=user)
    if category_name != '全部':
        blog_list = all_blog.filter(user=user, category__name=category_name)
    else:
        blog_list = all_blog
    catalog = blog_list.order_by('-top', '-star', '-publish_date', '-blog_id')[
              CATALOG_COUNT_PER_PAGE * (current_page - 1):
              CATALOG_COUNT_PER_PAGE * current_page]

    # 获得博客分类对应的博客数量
    blog_category_count = [{
                               'category_id': category.category_id,
                               'name': category.name,
                               'count': category.blog_category.count()
                           } for category in category_list]
    default_bcc_count = 0
    for bcc in blog_category_count:
        if bcc['name'] == '默认分类':
            default_bcc_count = bcc['count']
            break
    # 页码总数
    page_size = int(ceil(blog_list.count() / CATALOG_COUNT_PER_PAGE))

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
        'page_size': page_size,
        'category_name': category_name,
        'category_list': blog_category_count,
        'blog_count': blog_list.count(),
        'default_count': default_bcc_count
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


@authorize()
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


@authorize()
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
            is_top = request.POST['top']
            is_star = request.POST['star']
            level = request.POST['level']
            key_words = request.POST['keyWords']
        except KeyError:
            logger.debug('* 带非法参数请求，已经拒绝用户')
            raise Http404

        logger.debug('* BLOG TITLE:' + blog_title)
        logger.debug('* BLOG CONTENT:' + blog_content)
        logger.debug('* BLOG CATALOG:' + category)
        logger.debug('* BLOG TOP:' + is_top)
        logger.debug('* BLOG STAR:' + is_star)
        logger.debug('* BLOG LEVEL:' + level)
        logger.debug('* BLOG KEYS:' + key_words)
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
            blog.category = BlogCategory.objects.filter(user=user, category_id=category).first()
            blog.keywords = key_words
            blog.level = level
            blog.star = is_star == 'true'
            blog.top = is_top == 'true'
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


# **********************************************************************************************************************
# 博客分类管理处理
# **********************************************************************************************************************
@authorize()
def category_manage(request, whose):
    # TODO:博客分类管理
    # 跳转到分类管理页面，在该页面中能够添加/修改已经存在的博客分类
    # 同时允许创建专题分类，在专题分类中，能够调整菜单的层级
    #
    #
    # 专题分类的特点：本质是悬挂菜单资源，用户能够自行创建菜单资源，专题菜单的菜单资源关联到博客分类
    # 用户点击专题菜单时，实际上是点击分类，只有叶子节点能够点击并进行跳转
    #
    # 专题分类的创建过程：点击创建专题-->创建（允许创建子专题）-->创建成功后跳转到专题菜单的调整页面-->专题菜单调整后
    return render(request, 'blog/categoryManager.html')


@authorize()
def create_subject(request, whose):
    # TODO:创建专题菜单项
    """
    创建专题菜单项
    :param request:
    :param whose:
    :return:创建成功返回值为ok，否则返回值为failure
    """
    # 创建博客专题

    # 1、根据提供的名称创建博客分类
    # 2、根据提供的博客分类名称创建菜单资源，扩展字段中标记对应的博客分类的主键，关联专题菜单和博客分类，新创建的专题菜单
    # # #的父节点默认为根节点
    # 3、返回专题菜单的创建结果
    pass


@authorize()
def delete_subject(request, whose):
    # TODO:删除专题菜单项
    """
    删除专题菜单项
    :param request:
    :param whose:
    :return: 删除成功返回ok，失败返回failure
    """
    # 删除博客专题
    # 1、根据删除的博客专题菜单，判断是否是非叶子节点
    # # 如果是非叶子节点，继续搜索直到叶子节点，如果叶子节点对应的博客分类中包含了博文，提醒用户是否强制删除
    # # 如果是叶子节点，如果叶子节点对应的博客分类中包含了博文，提醒用户是否强制删除
    # 2、
    pass


@authorize()
def adjust_subject(request, whose):
    # TODO:调整专题菜单
    # 根据提交的菜单层级状况进行专题菜单的调整
    """
    调整专题菜单
    :param request:
    :param whose:
    :return:调整成功返回值为ok，否则返回值为failure
    """
    pass


@authorize()
def create_category(request, whose):
    # TODO:创建博客分类
    """
    创建博客分类
    :param request:
    :param whose:
    :return: 分类创建成功返回值为ok，否则返回值为failure
    """
    pass


@authorize()
def delete_category(request, whose):
    # TODO:删除博客分类
    """
    删除博客分类
    :param request:
    :param whose:
    :return:
    """
    pass


@authorize()
def update_category(request, whose):
    # TODO:更新一个博客分类信息
    """
    更新一个博客分类信息
    :param request:
    :param whose:
    :return: 更新成功返回值为ok，否则返回值为failure
    """
    pass


@authorize()
def update_subject(request, whose):
    # TODO:更新一个专题菜单
    """
    更新一个专题菜单
    :param request:
    :param whose:
    :return: 更新成功返回值为ok，否则返回值为failure
    """
    pass

# **********************************************************************************************************************
