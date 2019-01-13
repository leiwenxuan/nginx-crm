#!/usr/bin/env python
# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup


def get_font():
    # 使用requests模块发送get请求
    response = requests.get(
        url='http://fontawesome.dashgame.com/',
    )
    response.encoding = 'utf-8'
    # 使用BS4模块去解析获取的网页内容
    soup = BeautifulSoup(response.text, 'html.parser')
    web = soup.find(attrs={'id': 'web-application'})

    icon_list = []
    for item in web.find_all(attrs={'class': 'fa-hover'}):
        tag = item.find('i')
        class_name = tag.get('class')[1]
        icon_list.append([class_name, str(tag)])
    return icon_list
if __name__ == '__main__':
    print(get_font())
