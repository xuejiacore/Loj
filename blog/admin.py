from django.contrib import admin

from blog.models import Mood, BlogCategory, Blog, Comment

admin.site.register(Mood)
admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(Comment)
