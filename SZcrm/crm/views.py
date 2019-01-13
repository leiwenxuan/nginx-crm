# 导入日志
import logging
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse, QueryDict
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from crm.forms import Addfrom, EnrollmentForms, RecordForms, PaymentRecordForm
from crm.models import ConsultRecord, Customer, Enrollment, PaymentRecord
from utils import mypage
from SZcrm import settings

logger = logging.getLogger(__name__)

# Create your views here.


# 客户列表和我的客户列表
class IndexViews(View):
    '''
    程序分析：１．获取前端点击的页数
            2. 计算总的页数, 设置页面显示的数据量
            3. 计算要用多少页来显示　divmod(table_count, per_page)　商和余
            4. 处理下不是正确的页数
            5. 设置一个　页面显示多少页码
            ６. 处理页面显示各种特殊情况
            7. 拼接html 代码
    :param request:
    :return:
    '''

    # 获取操作的指令
    @method_decorator(login_required)
    def get(self, request):
        url_prefix = request.path_info
        print(url_prefix)
        # 深copy queryset 类型 11.22
        # qd = deepcopy(request.GET)
        # qd._mutable = True
        # request 自带copy  11.23
        qd = request.GET.copy()

        # 从URL获取参数
        current_page = request.GET.get("page", 1)
        if request.path_info == reverse('crm:pirvate'):
            # 私户
            customer_lsit = Customer.objects.filter(
                consultant=self.request.user)
            flag_page = 'pirvate'
        else:
            # 公户
            customer_lsit = Customer.objects.filter(consultant__isnull=True)
            flag_page = 'cus_list'
        # 模糊查找, 如果query为空不走模糊搜索
        if self.request.GET.get('query', ''):
            q = self._get_query_q(['name', 'qq', 'qq_name'])
            customer_lsit = customer_lsit.filter(q)

        # 总数据量
        table_count = customer_lsit.count()

        # 获取开始页和结束页
        page_obj = mypage.Pagination(current_page, table_count, url_prefix, qd)

        customer_lsit = customer_lsit[page_obj.start:page_obj.end]
        # 获取页面
        page_html = page_obj.page_html()

        # 11.23 获取当前的url
        url = request.get_full_path()
        query_params = QueryDict(mutable=True)
        query_params['next'] = url
        next_url = query_params.urlencode()
        data_dict = {
            'customer_list': customer_lsit,  # 传输的网页
            'next_url': next_url,  # 地址
            'page_list': page_html,  # 分页
            'flag_page': flag_page  # 点击页面样式flag
        }

        return render(request, 'index.html', data_dict)

    @method_decorator(login_required)
    def post(self, request):
        cid = request.POST.getlist('cid')
        print(cid)
        action = request.POST.get('action')
        # 反射 判断是否有一个_action 的方法有就执行没有， 返回一个提示
        if not hasattr(self, "_{}".format(action)):
            return HttpResponse("nihao")
        print(action, type(action))
        # 反射调用
        ret = getattr(self, '_{}'.format(action))(cid)
        if ret:
            return ret

        return redirect(reverse("crm:cus_list"))

    def _to_private(self, cid):
        # 计算传进来的cid 个数
        update_num = len(cid)
        # 判断我已经有的私户数量 + 这一次要提交的 < 我的私户
        # self.request.user.customer.count() 我的私户数量
        valid_num = (self.request.user.customers.count() + update_num) - 10
        if valid_num > 0:
            return HttpResponse(
                "做多还能添加{}多少好个".format(10 -
                                      self.request.user.customers.count()))

        # 考虑到多个销售抢一个客户的情况
        # 开启一个事务
        with transaction.atomic():
            # 方法1： 找到所有要操作的客户数据， 把他们变成我的客户
            select_objs = Customer.objects.filter(
                id__in=cid, consultant__isnull=True).select_for_update()
            select_num = select_objs.count()
            # 如果查询查询出来的数据不等于想要更新的数据， 说明被别人抢走了
            if select_num != update_num:
                # 拿到我可以死转化
                select_ids = [i[0] for i in select_objs.values_list('id')]
                select_objs.update(consultant=self.request.user)
                others = Customer.objects.filter(id__in=cid).exclude(
                    id__in=select_ids)
                name_tuple = others.values_list('name')
                name_str = ','.join([i[0] for i in name_tuple])
                return HttpResponse("手慢了， {}被抢走了".format(name_str))
            else:
                select_objs.update(consultant=self.request.user)

        # # 1 给我的客户列表添加 add函数
        # self.request.user.customers.add(*Customer.objects.filter(id__in=cid))
        # # 2 把要操作的客户添加到我的客户列表里
        # Customer.objects.filter(id__in=cid).update(
        #     consultant=self.request.user)

    def _to_all(self, cid):
        # 找到要操作的的客户，把他们的销售字段设置为空
        Customer.objects.filter(id__in=cid).update(consultant=None)
        # 或者从我的客户列表中把指定的客户删除
        # request.user.customers.remove(*Customer.objects.filter(id__in=cid)

    def _get_query_q(self, field_list, op="OR"):
        # 从GET请求的url中找到要检索的内容
        query_value = self.request.GET.get('query', '')
        q = Q()
        # 指定Q查询内部的操作是OR还是AND
        q.connector = op
        # 遍历要检索的字段， 挨个添加Q对象
        # field_list 传进来的一些自断
        for filed in field_list:
            # 模糊查找忽略大小写
            q.children.append(Q(('{}__icontains'.format(filed), query_value)))
        return q


# 添加和修改客户列表
class Add_cus(View):
    '''
    １．修改和增加一起操作
        思路利用formsmodel 操作, 修改和添加主要区别是id 问题，
        forms模块，　instance 可以等于None，在处理orm 获取对象时候，空QuerySet对象调用first为None
    '''

    @method_decorator(login_required)
    def get(self, request, cus_id=0):
        print(cus_id)
        cus_obj = Customer.objects.filter(id=cus_id).first()
        # print(cus_obj.consultant, type(cus_obj.consultant))
        form_obj = Addfrom(
            instance=cus_obj, initial={'consultant': request.user})
        return render(request, 'add_cus.html', {
            'form_obj': form_obj,
            'edit_id': cus_id
        })

    @method_decorator(login_required)
    def post(self, request, cus_id=0):
        # cus_id = request.GET.get('id')
        cus_obj = Customer.objects.filter(id=cus_id).first()
        print(cus_obj)

        form_obj = Addfrom(request.POST, instance=cus_obj)
        if form_obj.is_valid():
            form_obj.save()  # 保存的基础是调用上上一句实例话
            # url = reverse('crm:cus_list')
            # 如果能从URL获取到next参数就跳转到制定的URL,没有就默认跳转到客户列表页

            next_url = request.GET.get('next', reverse('crm:cus_list'))

            return redirect(next_url)
        else:
            return render(request, 'add_cus.html', {"form_obj": form_obj})


# 跟进客户
@login_required
def record_list(request):

    record_obj = ConsultRecord.objects.all()
    print(8888)
    return render(request, 'record_list.html', {
        "record_obj": record_obj,
        'flag_page': 'record_list'
    })


@login_required
def change_record(request):

    eidt_id = request.GET.get('edit_id', None)
    record_obj = ConsultRecord.objects.filter(id=eidt_id).first()
    if not record_obj:
        record_obj = ConsultRecord(consultant=request.user)
    form_obj = RecordForms(
        instance=record_obj, initial={'consultant': request.user})
    if request.method == 'POST':
        print(eidt_id)
        form_obj = RecordForms(request.POST, instance=record_obj)
        if form_obj.is_valid():
            form_obj.save()
            next_url = reverse('crm:record_list')
            print(next_url)
            return redirect(next_url)

    return render(request, 'edit_record.html', {
        "form_obj": form_obj,
        "edit_id": eidt_id
    })


# 跟进表
class EnrollmentViews(View):
    @method_decorator(login_required)
    def get(self, request, customer_id=0):
        if int(customer_id) == 0:
            # 1. 所有的客户列表
            Enr_obj = Enrollment.objects.filter(
                customer__consultant=request.user)
        else:
            # 查看当前的客户的跟进表
            Enr_obj = Enrollment.objects.filter(customer_id=customer_id)
        return render(request, 'en_list.html', {'enr_obj': Enr_obj})


# 修改跟进表
class enr_editViews(View):
    @method_decorator(login_required)
    def get(self, request, customer_id=0, enrollment_id=0):
        print(customer_id, enrollment_id)
        # 先根据 id区去查，如果为空说明新增
        enr_obj = Enrollment.objects.filter(id=enrollment_id).first()
        print(enr_obj, '修改')
        # 2.给表指定一个客户
        if not enr_obj:
            print('&' * 12)
            # 1.get 请求为添加操作， 先查看当前的要添加客户的对象
            customer_obj = Customer.objects.filter(id=customer_id).first()
            enr_obj = Enrollment(customer=customer_obj)

        form_obj = EnrollmentForms(instance=enr_obj)
        return render(request, 'enr_edit.html', {"form_obj": form_obj})

    @method_decorator(login_required)
    def post(self, request, customer_id=0, enrollment_id=0):
        # 获取要修改的对象
        print('#' * 120)
        # enr_obj = Enrollment(
        #     customer=(Customer.objects.filter(id=customer_id).first()))
        enr_obj = Enrollment.objects.filter(id=enrollment_id).first()
        print(enr_obj, customer_id)
        print(request.POST)
        # 实例化一个form对象
        form_obj = EnrollmentForms(request.POST, instance=enr_obj)
        print(form_obj.is_valid())
        if form_obj.is_valid():
            # 如果验证成功, 改变状态，
            # 1.获取一个对象
            enr_obj = form_obj.save()
            # 2.改变状态
            enr_obj.customer.status = 'signed'
            # 3.保存
            enr_obj.customer.save()

            print(
                reverse('crm:enrollment', kwargs={'customer_id': customer_id}))
            return redirect(
                reverse('crm:enrollment', kwargs={'customer_id': customer_id}))
            # return redirect(reverse('crm:enrollment'))
        else:
            print('enr_edit.html')
            return render(request, 'enr_edit.html', {"form_obj": form_obj})


# test cooladmin
def Coolindex(request):
    return render(request, 'CoolAdmin/index.html')


# 缴费记录
def payment(request, customer_id=0):
    # 根据用户id 找到他的缴费记录
    pay_obj = PaymentRecord.objects.filter(customer_id=customer_id)

    return render(request, 'pay_list.html', {"pay_obj": pay_obj})


# 编辑和添加缴费表
def edit_pay(request, customer_id=0):
    # 根据客户ｉｄ找到他的缴费记录
    pay_obj = PaymentRecord(customer_id=customer_id)
    # 有可能pay_obj 为none
    form_obj = PaymentRecordForm(instance=pay_obj)
    if request.method == "POST":
        form_obj = PaymentRecordForm(request.POST, instance=pay_obj)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(
                reverse('crm:payment', kwargs={'customer_id': customer_id}))

    return render(request, 'edit_pay.html', {"form_obj": form_obj})
