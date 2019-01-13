from django.conf.urls import url

from crm import auth_views, teacher_views, views

urlpatterns = [


    # 登陆相关
    url(r'^login/', auth_views.LoginViews.as_view(), name='login'),
    url(r'^v_code/', auth_views.v_code, name='v_code'),
    url(r'^log/', auth_views.login, name='log'),
    url(r'^reg/', auth_views.RegViews.as_view(), name='reg'),
    url(r'^check_user/', auth_views.check_user, name='check_user'),
    url(r'^logout/', auth_views.Logout.as_view(), name='logout'),
    url(r'^change/', auth_views.ChangeVires.as_view(), name='change'),

    # 极验滑动验证码 获取验证码的url
    url(r'^pc-geetest/register/', auth_views.get_geetest, name='register'),
    url(r'^get_valid_img.png/', auth_views.get_valid_img, name='get_valid_img'),

    # 客户相关
    url(r'^cus_list/', views.IndexViews.as_view(), name='cus_list'),
    url(r'^add_cus/(\d+)/$', views.Add_cus.as_view(), name='add_cus'),
    url(r'^edit_cus/(\d+)/$', views.Add_cus.as_view(), name='edit_cus'),  # all
    url(r'^private/', views.IndexViews.as_view(), name='pirvate'),  # 私户

    # 跟进表
    url(r'record_list/', views.record_list, name='record_list'),
    url(r'change_recode/', views.change_record, name='change_record'),

    # 报名表
    url(r'enrollment/(?P<customer_id>\d+)/$', views.EnrollmentViews.as_view(), name='enrollment'),
    url(r'enr_add/(?P<customer_id>\d+)/$', views.enr_editViews.as_view(), name='enr_add'),
    url(r'enr_edit/(?P<enrollment_id>\d+)/$', views.enr_editViews.as_view(), name='enr_edit'),


    # 班级url视图
    url(r'class_list/', teacher_views.ClasslistViews.as_view(), name='class_list'),
    url(r'add_class/(\d+)/$', teacher_views.add_list, name='add_list'),

    # 班级记录
    url(r'course_class/(?P<class_id>\d+)/$', teacher_views.CourseRecordviews.as_view(), name='courserecord'),
    url(r'add_course/(?P<class_id>\d+)/$', teacher_views.AddCourseViews.as_view(), name='add_course'),

    # 学生记录表视图
    url(r'student_list/(?P<course_record_id>\d+)/$', teacher_views.student_list, name='student_lislt'),

    # cooladmin
    url(r'coolindex', views.Coolindex, name='coolindex'),

    # 缴费记录
    url(r'payment/(?P<customer_id>\d+)/$', views.payment, name='payment'),
    url(r'edit_pay/(?P<customer_id>\d+)/$', views.edit_pay, name='edit_pay'),

]
