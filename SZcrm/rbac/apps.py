from django.apps import AppConfig


class PurviewConfig(AppConfig):
    name = 'rbac'
    verbose_name = '权限控制系统'

    def ready(self):
       import rbac.utils.signals