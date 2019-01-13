import re
from django import template
from SZcrm import settings

register = template.Library()


@register.inclusion_tag(filename='rbac/menu.html')
def meun_list(request):
    # １． 获取当前的url
    new_url = request.path_info
    # ２． 获取session　储存的session　key
    menu_key = getattr(settings, 'SECRET_MENU', 'menu_list')
    # 3. 获取session 里面的权限限定
    menu_dict = request.session.get(menu_key)
    # 4.　循环判断：如果当前的ｕｒｌ在权限里面加一个css样式，
    # del menu_dict['null']

    menu_dict = sorted(menu_dict.values(), key=lambda x: x['weight'])
    for menu in menu_dict:
        menu['class'] = 'hide'
        for child in menu['children']:
            if re.match(r'^{}$'.format(child['url']), new_url):
                child['class'] = 'active'
                menu['class'] = ''
    return {'menu_list': menu_dict}


# 生成面包屑导航
@register.inclusion_tag(filename='rbac/bread_curmb.html')
def bread_crumb(request):
    request.bread_crumb = [{'title': '首页', 'url': '#'}]
    print(request.bread_crumb)
    bread_crumb_list = request.bread_crumb

    return {'bread_crumb_list': bread_crumb_list}


# 自定义filter　实现按钮是否显示
@register.filter()
def has_permission(request, value):
    key = getattr(settings, 'PERMISSION_URL_KEY', 'permissions_url')
    permissions_dict = request.session.get(key, {})
    return value in permissions_dict
