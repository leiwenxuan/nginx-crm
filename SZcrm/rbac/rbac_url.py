from django.conf.urls import url
from rbac import views

urlpatterns = [
    url(r'^role_list/$', views.role_list, name='role_list'),
    url(r'^add_role/$', views.edit_role, name='add_role'),
    url(r'^edit_role/(\d+)/$', views.edit_role, name='edit_role'),
    url(r'^del_role/(\d+)/$', views.del_role, name='del_role'),

    # 菜单列表
    url(r'^menu_list/$', views.menu_list, name='menu_list'),
    url(r'^add_menu/$', views.edit_meun, name='add_menu'),
    url(r'^edit_menu/(\d+)/$', views.edit_meun, name='edit_menu'),
    url(r'^del_menu/(\d+)/$', views.del_menu, name='del_menu'),

    # 权限列表
    url(r'^per_list', views.permission_list, name='per_list'),
    url(r'^per_edit/(\d+)/', views.edit_permission, name='edit_permission'),
    url(r'^per_add', views.edit_permission, name='add_permission'),
    url(r'^per_del/(\d+)/', views.del_permission, name='del_permission'),

    # 权限【批量导入
    url(r'^import_all/', views.import_all, name='import_all'),

    # 权限批量更新
    url(r'^process_update/$', views.Batch_processing, name='process_update'),
    url(r'time', views.time_001, name='time')
]
