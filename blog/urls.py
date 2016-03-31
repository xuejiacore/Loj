from django.conf.urls import url

from blog.views.blog.demoview import demo, ckeditor, upload_file, download_file
from blog.views.blog.blogViews import blog_editor, blog_publish, blog_catalog, blog_detail, blog_delete, blog_outline, \
    blog_create_category, blog_category

app_name = 'blog'

urlpatterns = [
    url(r'^demo/$', demo, name='demo'),
    url(r'^ck/$', ckeditor, name='ckeditor'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^download/$', download_file, name='download'),

    # 进入到博客的某一个视图中，在开发阶段可以进行配置
    # 博客分类创建
    url(r'^newcategory/$', blog_create_category, name='createCategory'),
    # 博客的概括内容（首页）
    url(r'^outline/$', blog_outline, name='outline'),
    # 博客编辑发表
    url(r'^editor/$', blog_editor, name='blogEditor'),
    url(r'^publish/$', blog_publish, name='publishBlog'),
    # 博客目录页
    url(r'^catalog/(?P<category>\w+)/(?P<page>\d+)/$', blog_catalog, name='blogCatalog'),
    # 博客详细内容页
    url(r'^(?P<blog_id>\w+)/content/$', blog_detail, name='blogDetail'),
    # 删除博客
    url(r'^(?P<blog_id>\w+)/delete/$', blog_delete, name='blogDelete'),
    # 博客分类管理
    url('^categories/$', blog_category, name='blogCategories')
]
