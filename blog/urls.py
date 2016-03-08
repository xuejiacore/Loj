from django.conf.urls import url

from blog.views.blog.demoview import demo, ckeditor, upload_file, download_file
from blog.views.blog.blogViews import blog_editor, blog_publish, blog_catalog, blog_detail, blog_delete

app_name = 'blog'

urlpatterns = [
    url(r'^demo/$', demo, name='demo'),
    url(r'^ck/$', ckeditor, name='ckeditor'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^download/$', download_file, name='download'),

    # 进入到博客的某一个视图中，在开发阶段可以进行配置
    # 博客编辑发表
    url(r'^editor/$', blog_editor, name='blogEditor'),
    url(r'^publish/$', blog_publish, name='publishBlog'),
    # 博客目录页
    url(r'^catalog/$', blog_catalog, name='blogCatalog'),
    # 博客详细内容页
    url(r'^(?P<blog_id>\w+)/content/$', blog_detail, name='blogDetail'),
    # 删除博客
    url(r'^(?P<blog_id>\w+)/delete/$', blog_delete, name='blogDelete'),

]
