from django.contrib import admin

from author.models import User, Resource, Role, RolePrivilege, Privilege, UserRole

admin.site.register(User)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Privilege)
admin.site.register(RolePrivilege)
admin.site.register(Resource)
