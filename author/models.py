import datetime

from django.db import models


# 创建Models


class User(models.Model):
    """
    用户表
    """
    user_id = models.AutoField('用户ID', primary_key=True)
    login_id = models.CharField('登陆名', max_length=30, unique=True, null=False, blank=False)
    password = models.CharField('登陆密码', max_length=32, null=False, blank=False)
    real_name = models.CharField('真实姓名', max_length=60, null=False, blank=False)
    status = models.IntegerField('状态', default=0, choices=((0, '启用'), (1, '冻结')), null=False, blank=False)
    creator = models.ForeignKey('self', verbose_name='注册人', related_name='creator_user', null=True, blank=True)
    reg_date = models.DateTimeField('注册时间', default=datetime.datetime.now(), null=False, blank=True)
    portrait = models.CharField('用户头像', max_length=255, null=True, blank=True)
    territory = models.CharField('领域', max_length=50, null=True, blank=True)
    email = models.EmailField('电子邮件', null=True, blank=True)
    phone = models.CharField('电话', max_length=20, null=True, blank=True)
    updater = models.ForeignKey('self', verbose_name='更新人', related_name='updater_user', null=True, blank=True)
    update_date = models.DateTimeField('更新时间', null=True, blank=True)
    province_id = models.CharField('省份id', max_length=300, null=True, blank=True)
    level = models.IntegerField('等级', null=True, blank=True)
    extend_1 = models.CharField('扩展1', max_length=255, null=True, blank=True)
    extend_2 = models.CharField('扩展2', max_length=255, null=True, blank=True)
    extend_3 = models.CharField('扩展3', max_length=255, null=True, blank=True)
    extend_4 = models.CharField('扩展4', max_length=255, null=True, blank=True)
    extend_5 = models.CharField('扩展5', max_length=255, null=True, blank=True)
    extend_6 = models.BooleanField('扩展6', default=False, null=False, blank=True)

    class Meta:
        db_table = 'T_USER'
        verbose_name = "User"


class Role(models.Model):
    """
    角色表
    """
    role_code = models.AutoField('角色编码', primary_key=True)
    role_name = models.CharField('角色名称', max_length=50, null=False, blank=False)
    creator = models.ForeignKey(User, verbose_name='创建人', related_name='role_creator', null=False, blank=False)
    create_date = models.DateTimeField('创建时间', default=datetime.datetime.now(), null=False, blank=True)
    updater = models.ForeignKey(User, verbose_name='更新人', related_name='role_updater', null=True, blank=True)
    update_date = models.DateTimeField('更新时间', null=True, blank=True)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'T_ROLE'
        verbose_name = 'Role'


class Resource(models.Model):
    """
    资源表
    """
    res_id = models.AutoField('资源id', primary_key=True)
    res_type = models.IntegerField('资源类型')
    res_name = models.CharField('资源名称', max_length=50, null=False, blank=False)
    res_url = models.CharField('资源url', max_length=1024, null=False, blank=False)
    parent_node = models.ForeignKey('self', verbose_name='父节点', related_name='parent_resource', null=True, blank=True)
    remark = models.CharField('备注', max_length=255, null=True, blank=True)
    status = models.IntegerField('资源状态', default=0, null=False, blank=True)
    extend_1 = models.CharField('扩展字段1', max_length=30, null=True, blank=True)
    extend_2 = models.CharField('扩展字段2', max_length=64, null=True, blank=True)
    extend_3 = models.CharField('扩展字段3', max_length=128, null=True, blank=True)
    extend_4 = models.CharField('扩展字段4', max_length=128, null=True, blank=True)
    extend_5 = models.CharField('扩展字段5', max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'T_RESOURCE'
        verbose_name = 'Resource'


class Privilege(models.Model):
    """
    权限表
    """
    privilege_id = models.AutoField('权限ID', primary_key=True)
    res_id = models.ForeignKey(Resource, verbose_name='资源ID', related_name='privilege_resource', null=False,
                               blank=False)
    privilege_name = models.CharField('权限名称', max_length=30)
    pri_create = models.IntegerField('创建权限', choices=((0, '否'), (1, '是')), default=0, null=False, blank=True)
    pri_delete = models.IntegerField('删除权限', choices=((0, '否'), (2, '是')), default=0, null=False, blank=True)
    pri_access = models.IntegerField('访问权限', choices=((0, '否'), (4, '是')), default=0, null=False, blank=True)
    pri_modify = models.IntegerField('修改权限', choices=((0, '否'), (8, '是')), default=0, null=False, blank=True)
    pri_import = models.IntegerField('导入权限', choices=((0, '否'), (16, '是')), default=0, null=False, blank=True)
    pri_export = models.IntegerField('导出权限', choices=((0, '否'), (32, '是')), default=0, null=False, blank=True)
    extend_1 = models.IntegerField('扩展权限1', choices=((0, '否'), (64, '是')), default=0, null=False, blank=True)
    extend_2 = models.IntegerField('扩展权限2', choices=((0, '否'), (128, '是')), default=0, null=False, blank=True)
    extend_3 = models.IntegerField('扩展权限3', choices=((0, '否'), (256, '是')), default=0, null=False, blank=True)
    extend_4 = models.IntegerField('扩展权限4', choices=((0, '否'), (512, '是')), default=0, null=False, blank=True)

    class Meta:
        db_table = 'T_PRIVILEGE'
        verbose_name = 'Privilege'


class UserRole(models.Model):
    """
    用户角色表
    """
    user_role_id = models.AutoField('用户角色ID', primary_key=True)
    role = models.ForeignKey(Role, verbose_name='角色', related_name='user_m1_role', null=False, blank=False)
    user = models.ForeignKey(User, verbose_name='用户', related_name='user_m2_role', null=False, blank=False)

    class Meta:
        db_table = 'T_USER_ROLE'
        verbose_name = 'UserRole'


class RolePrivilege(models.Model):
    """
    角色权限表
    """
    role_pri_id = models.AutoField('角色权限ID', primary_key=True)
    privilege = models.ForeignKey(Privilege, verbose_name='权限', related_name='role_m1_privilege', null=False,
                                  blank=False)
    role = models.ForeignKey(Role, verbose_name='角色', related_name='role_m2_privilege', null=False, blank=False)

    class Meta:
        db_table = 'T_ROLE_PRIVILEGE'
        verbose_name = 'RolePrivilege'


class Grant(models.Model):
    """
    授权表
    """
    grant_id = models.AutoField('授权ID', primary_key=True)
    user = models.ForeignKey(User, verbose_name='用户', related_name='user_grant', null=False, blank=False)
    privilege = models.ForeignKey(Privilege, verbose_name='授权', related_name='grant_privilege', null=False, blank=False)

    class Meta:
        db_table = 'T_GRANT'
        verbose_name = 'Grant'
