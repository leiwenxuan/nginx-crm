from django.utils.deprecation import MiddlewareMixin
from SZcrm import settings
from django.shortcuts import HttpResponse, redirect
import re


class LoginMiddle(MiddlewareMixin):
    def process_request(self, request):
        # 1. 获取白名单，　没有找到为[]
        white_list = getattr(settings, 'WHITE_URLS', [])
        # 2. 获取当前的url
        new_url = request.path_info
        for url in white_list:
            if re.match(r'^{}$'.format(url), new_url):
                return None
        # 2. 获取session的里面设置url PERMISSION_URL_KEY = 'permissions_url'
        session_key = getattr(settings, 'PERMISSION_URL_KEY',
                              'permissions_url')
        # 面包屑生成
        # 1. 获取数据

        menu_key = getattr(settings, 'SECRET_MENU', 'menu_list')
        print(menu_key)
        menu_dict = request.session[menu_key]
        print(menu_dict)
     # ２面包屑　数据结构
        request.bread_crumb = [{'title': '首页', 'url': '#'}]
        print(request.bread_crumb, '&'*120)
        for item in request.session[session_key].values():
            if re.match(r'^{}$'.format(item['url']), new_url):
                # 根据权限找到父菜单，保存到request.bread_crumb里面
                menu_title = menu_dict[str(item['menu_id'])]['title']
                request.bread_crumb.append({'title': menu_title})
                return None
        else:
            return HttpResponse("没有此权限")





