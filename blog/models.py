import datetime

from django import forms
from django.db import models

from author.models import User


class BlogCategory(models.Model):
    """
    博文分类表
    """
    category_id = models.AutoField('类别ID', primary_key=True)
    user = models.ForeignKey(User, verbose_name='所属用户', related_name='user_blog_catalog', null=False, blank=False)
    name = models.CharField('类别名称', max_length=30, null=False, blank=False)
    create_date = models.DateTimeField('创建时间', default=datetime.datetime.now(), null=False, blank=True)
    update_date = models.DateTimeField('修改时间', null=True, blank=True)
    desc = models.CharField('类别描述', max_length=255, null=True, blank=False)
    level = models.IntegerField('优先级别', null=True, blank=True)

    class Meta:
        db_table = 'T_BLOG_CATEGORY'
        verbose_name = 'BlogCategory'


class Blog(models.Model):
    """
    博文内容表
    """
    blog_id = models.AutoField('博客ID', primary_key=True)
    user = models.ForeignKey(User, verbose_name='所属用户', related_name='user_blog', null=False, blank=False)
    category = models.ForeignKey(BlogCategory, verbose_name='所属类别', related_name='blog_category', null=False, blank=False)
    publish_date = models.DateTimeField('发布时间', default=datetime.datetime.now(), null=False, blank=True)
    publish_ip = models.GenericIPAddressField('发布ip', max_length=40, null=True, blank=True)
    update_date = models.DateTimeField('修改时间', null=True, blank=True)
    blog_title = models.CharField('博客标题', max_length=30, null=False, blank=False)
    keywords = models.CharField('关键字', max_length=512, null=True, blank=True)
    blog_content = models.TextField('内容', null=False, blank=False)
    status = models.IntegerField('发布状态', default=0, null=False, blank=True)
    privilege = models.IntegerField('评论权限', default=1, null=False, blank=True)
    level = models.IntegerField('隐私级别', default=0, null=False, blank=True)
    read_times = models.IntegerField('阅读次数', default=0, null=False, blank=False)
    replied_times = models.IntegerField('回复次数', default=0, null=False, blank=False)
    top = models.BooleanField('是否置顶', choices=((True, '是'), (False, '否')), default=False, null=False, blank=True)
    star = models.IntegerField('星标', choices=((1, '是'), (0, '否')), default=False, null=False, blank=True)

    class Meta:
        db_table = 'T_BLOG'
        verbose_name = 'Blog'


class Mood(models.Model):
    """
    心情表
    """
    mood_id = models.AutoField('心情ID', primary_key=True)
    user = models.ForeignKey(User, verbose_name='所属用户', related_name='user_mood', null=False, blank=False)
    create_date = models.DateTimeField('创建时间', default=datetime.datetime.now(), null=False, blank=False)
    content = models.CharField('内容', max_length=2048, null=False, blank=False)
    level = models.IntegerField('隐私级别', null=False, blank=False)

    class Meta:
        db_table = 'T_MOOD'
        verbose_name = 'Mood'


class Comment(models.Model):
    """
    评论表
    """
    comment_id = models.AutoField('评论ID', primary_key=True)
    user = models.ForeignKey(User, verbose_name='所属用户', related_name='user_blog_comment', null=True, blank=True)
    blog = models.ForeignKey(Blog, verbose_name='评论博文', related_name='blog_comment', null=True, blank=True)
    mood = models.ForeignKey(Mood, verbose_name='评论心情', related_name='mood_comment', null=True, blank=True)
    reply = models.ForeignKey('self', verbose_name='回复评论', related_name='reply_comment', null=True, blank=True)
    content = models.CharField('评论内容', max_length=1024, null=False, blank=False)
    reply_date = models.DateTimeField('评论时间', default=datetime.datetime.now(), null=False, blank=False)
    reply_up = models.GenericIPAddressField('评论者IP', max_length=40, null=True, blank=True)

    class Meta:
        db_table = 'T_COMMENT'
        verbose_name = 'Comment'


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
