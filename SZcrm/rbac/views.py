from django.shortcuts import render, redirect, HttpResponse
from rbac import models
from rbac.utils import reload_routes
from django.urls import reverse
from crm.models import UserProfile
from rbac.forms import RoleForm, MenuForm, UserpurviewForm
#  formset_factory　数据库不存在，　在保存时必须手动创建
#  modelform_factory 修改编辑
from django.forms import modelformset_factory, formset_factory, modelform_factory
from rbac.utils import signals

from utils import mypage

# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pwd = request.POST.get("password")
        user_obj = UserProfile.objects.filter(
            username=username, password=pwd).first()
        print(username, pwd, user_obj)
        if user_obj:
            # 登陆成功
            from rbac.utils import permission
            permission.init(request, user_obj)
            return redirect(reverse('web:customer_list'))

    return render(request, 'login.html')


# TODO: 2018-11-26 2:50
def logout(request):
    print(request.session)
    request.session.flush()
    return redirect(reverse('login'))


# 角色列表
def role_list(request):
    role_obj = models.Role.objects.all()
    return render(request, 'role_list.html', {'role_obj': role_obj})


def edit_role(request, edit_id=0):
    role_obj = models.Role.objects.filter(id=edit_id).first()
    form_obj = RoleForm(instance=role_obj)
    if request.method == 'POST':
        form_obj = RoleForm(request.POST, instance=role_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:role_list'))
    return render(request, 'add_role.html', {'form_obj': form_obj})


def del_role(request, edit_id=None):
    models.Role.objects.filter(pk=edit_id).delete()
    return redirect(reverse('rbac:role_list'))


# 菜单
def menu_list(request):
    menu_obj = models.Menu.objects.all()
    # role_obj = models.Role.objects.all()
    per_obj = models.Userpurview.objects.all()
    return render(request, 'menu_list.html', {
        'menu_obj': menu_obj,
        'per_obj': per_obj
    })


def edit_meun(request, edit_id=None):
    menu_obj = models.Menu.objects.filter(pk=edit_id).first()
    form_obj = MenuForm(instance=menu_obj)
    if request.method == 'POST':
        print(request.POST)
        form_obj = MenuForm(request.POST, instance=menu_obj)
        print(form_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(reverse('rbac:menu_list'))
        else:
            print('&' * 20)
            print(form_obj)
            return render(request, 'add_menu.html', {'form_obj': form_obj})
    return render(request, 'add_menu.html', {'form_obj': form_obj})


def del_menu(request, edit_id=None):
    models.Menu.objects.filter(pk=edit_id).delete()
    return redirect(reverse('rbac:menu_list'))


# 权限列表
def permission_list(request):
    per_obj = models.Userpurview.objects.all()
    return render(request, 'permission_list.html', {'per_obj': per_obj})


def edit_permission(request, edit_id=None):
    menu_obj = models.Userpurview.objects.filter(pk=edit_id).first()
    form_obj = UserpurviewForm(instance=menu_obj)
    if request.method == 'POST':
        print(request.POST)
        form_obj = UserpurviewForm(request.POST, instance=menu_obj)
        print(form_obj)
        if form_obj.is_valid():
            form_obj.save()
            signals.pizza_done.send(sender='save', request=request, obj=request.user)
            return redirect(reverse('rbac:menu_list'))
        else:
            print('&' * 20)
            print(form_obj)
            return render(request, 'add_menu.html', {'form_obj': form_obj})
    return render(request, 'add_menu.html', {'form_obj': form_obj})


def del_permission(request, edit_id=None):
    models.Userpurview.objects.filter(pk=edit_id).delete()
    next_url = request.GET.get('next', 'rbac:menu_list')
    return redirect(next_url)


# 权限导入
def import_all(request):
    # 1.2 调用脚本, 读取项目中的所有的路由
    all_url = reload_routes.get_all_url_dict(
        ignore_namespace_list=['admin', '__debug__'])
    # １.2 读取数据库里面的路由
    all_permissions = models.Userpurview.objects.all()
    # 用集合去判断
    # 项目的url
    project_url_set = set(all_url.keys())
    # 数据库的ｕｒｌ
    db_ulr_set = set([i.name for i in all_permissions])

    # 1.项目有，数据库没有
    pro_db = project_url_set - db_ulr_set
    data_init = [v for k, v in all_url.items() if k in pro_db][:5]
    addFormset = formset_factory(UserpurviewForm, extra=0)
    add_formset_obj = addFormset(initial=data_init)

    # 2. 权限表里有，项目里面也有
    pro_and_db = project_url_set & db_ulr_set
    data_init_all = models.Userpurview.objects.filter(name__in=pro_and_db)
    addFormset_all = modelformset_factory(
        models.Userpurview, UserpurviewForm, extra=0)
    add_formset_all = addFormset_all(queryset=data_init_all, )

    if request.method == 'POST':
        print(request.GET.get('post_type'))
        # 如果是添加操作
        if request.GET.get('post_type') == 'add':
            add_formset_obj = addFormset(request.POST)
            if add_formset_obj.is_valid():
                add_obj = (models.Userpurview(**items)
                           for items in add_formset_obj.cleaned_data)
                models.Userpurview.objects.bulk_create(add_obj)
        # 如果是修改
        if request.GET.get('post_type') == 'edit':
            print('edit')
            add_formset_all = addFormset_all(
                request.POST, queryset=data_init_all)
            if add_formset_all.is_valid():
                print('edit' * 20)
                add_formset_all.save()

        return redirect(reverse('rbac:import_all'))

    # 3. 权限表没有，项目有
    db_pro = db_ulr_set - project_url_set
    data_init_db = models.Userpurview.objects.filter(name__in=db_pro)
    add_formset_db = addFormset_all(queryset=data_init_db)
    seed_url_dict = {
        'add_formset_obj': add_formset_obj,
        'add_formset_all': add_formset_all,
        'add_formset_db': add_formset_db,
    }

    return render(request, 'permission_Batch.html', seed_url_dict)


# 批量权限处理
def Batch_processing(request):
    # 查找所有的用户
    user_obj = UserProfile.objects.all()
    # 查找所有的角色
    role_obj = models.Role.objects.all()
    # 查找所有的菜单
    menu_obj = models.Menu.objects.all()

    # 获取user_id
    user_id = request.GET.get('user_id')
    user_id_obj = UserProfile.objects.filter(pk=user_id).first()

    # 获取role_id
    role_id = request.GET.get('role_id')
    print(role_id, '&' * 20)
    role_id_obj = models.Role.objects.filter(pk=role_id).first()
    # if is post
    if request.method == 'POST':
        print(request.POST.get('type_post'), 8888)
        if request.POST.get('type_post') == 'role_set':
            # get Role input checked
            print(777)
            role_ids = request.POST.getlist('role_id')
            user_id_obj.roles.set(models.Role.objects.filter(id__in=role_ids))

        if request.POST.get('type_post') == 'process_set':
            process_ids = request.POST.getlist('process_id')
            role_id_obj.permissions.set(
                models.Userpurview.objects.filter(id__in=process_ids))


    seed_data = {
        'user_obj': user_obj,
        'role_obj': role_obj,
        'menu_obj': menu_obj,
        'user_id_obj': user_id_obj,
        'role_id_obj': role_id_obj
    }
    return render(request, 'processing_batch.html', seed_data)


import json
# 缓存test程序 2018-12-1
def time_001(request):
    # 获取菜单选项
    # ret = models.Menu.objects.all().first()
    # json_ret = json.dumps(ret)
    # print(json_ret)
    import time
    now = time.asctime()
    # 查询一个url所属权限
    obj = models.Userpurview.objects.all().first()

    return render(request, 'time_001.html', {"now": now})

#
# import r
# def v_code(request):
#     with open('1.jpg', 'wb') as f:
