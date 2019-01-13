a = {
    '1': {
        'id':
        1,
        'title':
        '客户管理',
        'icon':
        'fa-address-card-o',
        'weight':
        200,
        'children': [{
            'title': '查看客户',
            'url': '/crm/cus_list/',
            'show': True
        }, {
            'title': '添加客户',
            'url': '/crm/add_cus/',
            'show': True
        }, {
            'title': '我的私户',
            'url': '/crm/private/',
            'show': False
        }, {
            'title': '跟进客户',
            'url': '/crm/record_list/',
            'show': False
        }, {
            'title': '修改和添加',
            'url': '/crm/change_recode/',
            'show': False
        },
                     {
                         'title': '报名表',
                         'url': '/crm/enrollment/(?P<customer_id>\\d+)/',
                         'show': True
                     },
                     {
                         'title': '添加报名表',
                         'url': '/crm/enr_add/(?P<customer_id>\\d+)/',
                         'show': True
                     },
                     {
                         'title': '修改报名表',
                         'url': '/crm/enr_edit/(?P<enrollment_id>\\d+)/',
                         'show': False
                     }]
    },
    '3': {
        'id':
        3,
        'title':
        '班级管理',
        'icon':
        'fa-bank',
        'weight':
        100,
        'children': [{
            'title': '添加班级',
            'url': '/crm/add_class/(\\d+)/',
            'show': True
        },
                     {
                         'title': '添加班级记录',
                         'url': '/crm/add_course/(?P<class_id>\\d+)/',
                         'show': True
                     },
                     {
                         'title': '查看班级',
                         'url': '/crm/class_list/',
                         'show': True
                     },
                     {
                         'title': '班级记录',
                         'url': '/crm/course_class/(?P<class_id>\\d+)/',
                         'show': True
                     },
                     {
                         'title': '学习考勤',
                         'url':
                         '/crm/student_list/(?P<course_record_id>\\d+)/',
                         'show': True
                     },
                     {
                         'title': '缴费记录',
                         'url': '/crm/payment/(?P<customer_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '修改缴费记录',
                         'url': '/crm/edit_pay/(?P<customer_id>\\d+)/',
                         'show': False
                     }]
    },
    '4': {
        'id':
        4,
        'title':
        'RBAC控制',
        'icon':
        'fa-address-book',
        'weight':
        56,
        'children': [{
            'title': '角色列表',
            'url': '/rbac/role_list/',
            'show': True
        }, {
            'title': '菜单列表',
            'url': '/rbac/menu_list/',
            'show': True
        }, {
            'title': '添加菜单',
            'url': '/rbac/add_menu/',
            'show': False
        }, {
            'title': '修改角色',
            'url': '/rbac/edit_role/(\\d+)/',
            'show': False
        }, {
            'title': '权限列表',
            'url': '/rbac/per_list/',
            'show': False
        }, {
            'title': '删除角色',
            'url': '/rbac/del_role/(\\d+)/',
            'show': False
        }, {
            'title': '修改菜单',
            'url': '/rbac/edit_menu/(\\d+)/',
            'show': False
        }, {
            'title': '删除菜单',
            'url': '/rbac/del_menu/(\\d+)/',
            'show': False
        }, {
            'title': '修改权限',
            'url': '/rbac/per_edit/(\\d+)/',
            'show': False
        }, {
            'title': '添加权限',
            'url': '/rbac/per_add',
            'show': False
        }, {
            'title': '删除权限',
            'url': '/rbac/per_del/(\\d+)/',
            'show': False
        }, {
            'title': '显示权限列表',
            'url': '/rbac/import_all/',
            'show': True
        }]
    },
    '6': {
        'id':
        6,
        'title':
        '登陆',
        'icon':
        'fa-drivers-lice',
        'weight':
        50,
        'children': [{
            'title': '校验',
            'url': '/crm/check_user/',
            'show': False
        }, {
            'title': '注销',
            'url': '/crm/logout/',
            'show': False
        }, {
            'title': '修改密码',
            'url': '/crm/change/',
            'show': False
        }, {
            'title': '极限',
            'url': '/crm/pc-geetest/register/',
            'show': False
        }, {
            'title': '极限',
            'url': '/crm/get_valid_img.png/',
            'show': False
        }]
    },
    'null': {
        'id': None,
        'title': None,
        'icon': None,
        'weight': None,
        'children': [{
            'title': '添加角色',
            'url': '/rbac/add_role/',
            'show': False
        }]
    }
}

b = {
    10: {
        'id':
        10,
        'title':
        '登陆',
        'icon':
        'fa-id-card',
        'weight':
        50,
        'children': [{
            'title': '11',
            'url': '/__debug__/sql_profile/',
            'show': False
        }, {
            'title': '11',
            'url': '/__debug__/template_source/',
            'show': False
        }, {
            'title': '登陆',
            'url': '/crm/login/',
            'show': False
        }, {
            'title': '极限登陆',
            'url': '/crm/log/',
            'show': False
        }, {
            'title': '注册',
            'url': '/crm/reg/',
            'show': False
        }, {
            'title': '检验',
            'url': '/crm/check_user/',
            'show': False
        }, {
            'title': '注销',
            'url': '/crm/logout/',
            'show': True
        }, {
            'title': '修改密码',
            'url': '/crm/change/',
            'show': True
        }, {
            'title': '11',
            'url': '/crm/pc-geetest/register/',
            'show': False
        }]
    },
    9: {
        'id':
        9,
        'title':
        '客户管理',
        'icon':
        'fa-address-book',
        'weight':
        50,
        'children': [{
            'title': '客户列表',
            'url': '/crm/cus_list/',
            'show': False
        }, {
            'title': '添加客户',
            'url': '/crm/add_cus/',
            'show': False
        }, {
            'title': '修改客户',
            'url': '/crm/edit_cus/(\\d+)/',
            'show': False
        }, {
            'title': '我的私户',
            'url': '/crm/private/',
            'show': True
        }, {
            'title': '跟进表',
            'url': '/crm/record_list/',
            'show': True
        }, {
            'title': '修改跟进表',
            'url': '/crm/change_recode/',
            'show': False
        },
                     {
                         'title': '报名表',
                         'url': '/crm/enrollment/(?P<customer_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '添加报名表',
                         'url': '/crm/enr_add/(?P<customer_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '修改报名表',
                         'url': '/crm/enr_edit/(?P<enrollment_id>\\d+)/',
                         'show': False
                     }]
    },
    11: {
        'id':
        11,
        'title':
        '班级管理',
        'icon':
        'fa-drivers-lice',
        'weight':
        50,
        'children': [{
            'title': '班级列表',
            'url': '/crm/class_list/',
            'show': True
        }, {
            'title': '添加班级',
            'url': '/crm/add_class/(\\d+)/',
            'show': True
        },
                     {
                         'title': '班级记录',
                         'url': '/crm/course_class/(?P<class_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '添加班级记录',
                         'url': '/crm/add_course/(?P<class_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '学生考勤',
                         'url':
                         '/crm/student_list/(?P<course_record_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '缴费记录',
                         'url': '/crm/payment/(?P<customer_id>\\d+)/',
                         'show': False
                     },
                     {
                         'title': '修改缴费记录',
                         'url': '/crm/edit_pay/(?P<customer_id>\\d+)/',
                         'show': False
                     }]
    },
    12: {
        'id':
        12,
        'title':
        'RBAC控制',
        'icon':
        'fa-drivers-lice',
        'weight':
        50,
        'children': [{
            'title': '修改角色',
            'url': '/rbac/edit_role/(\\d+)/',
            'show': False
        }, {
            'title': '删除角色',
            'url': '/rbac/del_role/(\\d+)/',
            'show': False
        }, {
            'title': '菜单列表',
            'url': '/rbac/menu_list/',
            'show': True
        }, {
            'title': '添加菜单',
            'url': '/rbac/add_menu/',
            'show': False
        }, {
            'title': '修改菜单',
            'url': '/rbac/edit_menu/(\\d+)/',
            'show': False
        }, {
            'title': '删除菜单',
            'url': '/rbac/del_menu/(\\d+)/',
            'show': False
        }, {
            'title': '权限列表',
            'url': '/rbac/per_list',
            'show': True
        }, {
            'title': '修改权限列表',
            'url': '/rbac/per_edit/(\\d+)/',
            'show': False
        }, {
            'title': '添加权限列表',
            'url': '/rbac/per_add',
            'show': False
        }, {
            'title': '批量处理权限',
            'url': '/rbac/import_all/',
            'show': True
        }, {
            'title': '批量更新权限',
            'url': '/rbac/process_update/',
            'show': True
        }]
    }
}
