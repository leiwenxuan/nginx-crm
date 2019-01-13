"""
RBAC组件
权限相关的模块
"""
# from django.conf import settings

from SZcrm import settings


def init(request, user_obj):
    """
    根据当前登录的用户初始化权限信息和菜单信息，保存到session中
    :param request: 请求对象
    :param user_obj: 登陆的用户对象
    :return:
    """
    # 1. 将当前登录用户的权限信息查询出来
    queryset = user_obj.roles.all().filter(permissions__isnull=False).values(
        'permissions__url',  # 权限的URL
        'permissions__title',  # 权限的名称
        'permissions__name',  # 路由别名
        'permissions__show',  # 权限是否显示
        'permissions__menu_id',  # 菜单的id
        'permissions__menu__title',  # 菜单的标题
        'permissions__menu__icon',  # 菜单的图标
        'permissions__menu__weight',  # 菜单的权重
    ).distinct()
    #[{'permissions__url': '/customer/list/', 'permissions__title': '客户列表', 'permissions__show': True, 'permissions__menu_id': 1, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-cc'}, {'permissions__url': '/customer/add/', 'permissions__title': '添加客户', 'permissions__show': True, 'permissions__menu_id': 1, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-cc'}, {'permissions__url': '/customer/edit/(?P<cid>\\d+)/', 'permissions__title': '编辑客户', 'permissions__show': False, 'permissions__menu_id': 1, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-cc'}, {'permissions__url': '/customer/del/(?P<cid>\\d+)/', 'permissions__title': '删除客户', 'permissions__show': False, 'permissions__menu_id': 1, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-cc'}, {'permissions__url': '/customer/import/$', 'permissions__title': '批量导入', 'permissions__show': False, 'permissions__menu_id': 1, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-cc'}, {'permissions__url': '/customer/tpl/', 'permissions__title': '下载模板', 'permissions__show': False, 'permissions__menu_id': 1, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-cc'}, {'permissions__url': '/payment/list/', 'permissions__title': '账单列表', 'permissions__show': True, 'permissions__menu_id': 2, 'permissions__menu__title': '账单管理', 'permissions__menu__icon': 'fa-heart'}, {'permissions__url': '/payment/add/', 'permissions__title': '添加账单', 'permissions__show': True, 'permissions__menu_id': 2, 'permissions__menu__title': '账单管理', 'permissions__menu__icon': 'fa-heart'}, {'permissions__url': '/payment/edit/', 'permissions__title': '编辑账单', 'permissions__show': False, 'permissions__menu_id': 2, 'permissions__menu__title': '账单管理', 'permissions__menu__icon': 'fa-heart'}, {'permissions__url': '/payment/del/', 'permissions__title': '删除账单', 'permissions__show': False, 'permissions__menu_id': 2, 'permissions__menu__title': '账单管理', 'permissions__menu__icon': 'fa-heart'}]>

    # 先取到权限列表
    permission_dict = {}
    # 存放菜单信息的列表
    menu_dict = {}
    for item in queryset:
        dict_key = item['permissions__name']
        permission_dict[dict_key] = {
            'url': item['permissions__url'],
            'menu_id': item['permissions__menu_id']
        }  # 能够访问的权限列表

        # 再取出菜单列表
        p_id = item['permissions__menu_id']
        if p_id not in menu_dict:
            menu_dict[p_id] = {
                'id':
                p_id,
                'title':
                item['permissions__menu__title'],
                'icon':
                item['permissions__menu__icon'],
                'weight':
                item['permissions__menu__weight'],
                'children': [{
                    'title': item['permissions__title'],
                    'url': item['permissions__url'],
                    'show': item['permissions__show']
                }]
            }
        else:
            menu_dict[p_id]['children'].append({
                'title':
                item['permissions__title'],
                'url':
                item['permissions__url'],
                'show':
                item['permissions__show']
            })

    # 2. 将权限信息保存到session数据中
    permission_key = getattr(settings, 'PERMISSION_URL_KEY', 'permissions_url')
    menu_key = getattr(settings, 'SECRET_MENU', 'menu_list')
    request.session[permission_key] = permission_dict
    # 3. 存菜单信息到session数据中
    request.session[menu_key] = menu_dict
    print(menu_dict)
