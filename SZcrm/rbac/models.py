from django.db import models
from crm.models import UserProfile

# Create your models here.


# 菜单栏
class Menu(models.Model):
    title = models.CharField(max_length=24, verbose_name='菜单名称')
    icon = models.CharField(max_length=24, null=True, blank=True)
    weight = models.PositiveIntegerField(default=50, verbose_name='菜单权重')

    class Meta:
        verbose_name = '菜单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 权限表
class Userpurview(models.Model):
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=80)
    show = models.BooleanField(default=False)
    menu = models.ForeignKey(
        to='Menu', verbose_name='所属菜单', null=True, blank=True)
    name = models.CharField(max_length=24, verbose_name='路由别名', unique=True)

    class Meta:
        verbose_name = '权限控制'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


# 角色表


class Role(models.Model):
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to='UserPurview')
    user = models.ManyToManyField(to=UserProfile, related_name='roles')

    class Meta:
        verbose_name = '角色控制'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
