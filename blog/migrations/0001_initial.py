# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-01 03:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0002_auto_20160301_1113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False, verbose_name='博客ID')),
                ('publish_date', models.DateTimeField(blank=True, default=datetime.datetime(2016, 3, 1, 11, 13, 51, 227902), verbose_name='发布时间')),
                ('publish_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='发布ip')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='修改时间')),
                ('blog_title', models.CharField(max_length=30, verbose_name='博客标题')),
                ('keywords', models.CharField(blank=True, max_length=512, null=True, verbose_name='关键字')),
                ('blog_content', models.TextField(verbose_name='内容')),
                ('status', models.IntegerField(blank=True, default=0, verbose_name='发布状态')),
                ('privilege', models.IntegerField(blank=True, default=1, verbose_name='评论权限')),
                ('level', models.IntegerField(blank=True, default=0, verbose_name='隐私级别')),
                ('read_times', models.IntegerField(default=0, verbose_name='阅读次数')),
                ('replied_times', models.IntegerField(default=0, verbose_name='回复次数')),
                ('top', models.BooleanField(choices=[(True, '是'), (False, '否')], default=False, verbose_name='是否置顶')),
                ('star', models.IntegerField(blank=True, choices=[(1, '是'), (0, '否')], default=False, verbose_name='星标')),
            ],
            options={
                'db_table': 'T_BLOG',
                'verbose_name': 'Blog',
            },
        ),
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False, verbose_name='类别ID')),
                ('name', models.CharField(max_length=30, verbose_name='类别名称')),
                ('create_date', models.DateTimeField(blank=True, default=datetime.datetime(2016, 3, 1, 11, 13, 51, 226919), verbose_name='创建时间')),
                ('update_date', models.DateTimeField(blank=True, null=True, verbose_name='修改时间')),
                ('desc', models.CharField(max_length=255, null=True, verbose_name='类别描述')),
                ('level', models.IntegerField(blank=True, null=True, verbose_name='优先级别')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_blog_catalog', to='author.User', verbose_name='所属用户')),
            ],
            options={
                'db_table': 'T_BLOG_CATEGORY',
                'verbose_name': 'BlogCategory',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(primary_key=True, serialize=False, verbose_name='评论ID')),
                ('content', models.CharField(max_length=1024, verbose_name='评论内容')),
                ('reply_date', models.DateTimeField(default=datetime.datetime(2016, 3, 1, 11, 13, 51, 228903), verbose_name='评论时间')),
                ('reply_up', models.GenericIPAddressField(blank=True, null=True, verbose_name='评论者IP')),
                ('blog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='blog_comment', to='blog.Blog', verbose_name='评论博文')),
            ],
            options={
                'db_table': 'T_COMMENT',
                'verbose_name': 'Comment',
            },
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('mood_id', models.AutoField(primary_key=True, serialize=False, verbose_name='心情ID')),
                ('create_date', models.DateTimeField(default=datetime.datetime(2016, 3, 1, 11, 13, 51, 228903), verbose_name='创建时间')),
                ('content', models.CharField(max_length=2048, verbose_name='内容')),
                ('level', models.IntegerField(verbose_name='隐私级别')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_mood', to='author.User', verbose_name='所属用户')),
            ],
            options={
                'db_table': 'T_MOOD',
                'verbose_name': 'Mood',
            },
        ),
        migrations.AddField(
            model_name='comment',
            name='mood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mood_comment', to='blog.Mood', verbose_name='评论心情'),
        ),
        migrations.AddField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_comment', to='blog.Comment', verbose_name='回复评论'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_blog_comment', to='author.User', verbose_name='所属用户'),
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_category', to='blog.BlogCategory', verbose_name='所属类别'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_blog', to='author.User', verbose_name='所属用户'),
        ),
    ]
