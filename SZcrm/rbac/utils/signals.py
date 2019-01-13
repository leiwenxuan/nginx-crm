# 信号初识
# from django.core.signals import request_finished
# from django.core.signals import request_started
# from django.core.signals import got_request_exception

# from django.db.models.signals import class_prepared
# from django.db.models.signals import pre_init, post_init
# from django.db.models.signals import pre_save, post_save
# from django.db.models.signals import pre_delete, post_delete
#
# from django.db.models.signals import pre_migrate, post_migrate
#
# from django.test.signals import setting_changed
# from django.test.signals import template_rendered
#
# from django.db.backends.signals import connection_created
#
# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver

# @receiver(post_save, sender=Userpurview)
# def callback(sender, **kwargs):
#     print(sender)
#     print(kwargs)
#     print("改动了权限设置")

# m2m_changed.connect(callback)


from django.dispatch import receiver
import django.dispatch
pizza_done = django.dispatch.Signal(providing_args=["request", "obj"])
from rbac.utils import permission


@receiver(pizza_done)
def callback(sender, **kwargs):
    print(sender)
    print(kwargs)
    request = kwargs['request']
    user_obj = kwargs['obj']
    permission.init(request, user_obj)
    print("改动了权限设置")
