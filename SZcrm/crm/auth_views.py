# 导入日志
import logging

from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.views import View
from geetest import GeetestLib
from rbac.utils import permission

from crm.forms import RegisteredForm
from crm.models import UserProfile
import random
from PIL import ImageFont, ImageDraw, Image

logger = logging.getLogger(__name__)


def random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def v_code(request):
    img_obj = Image.new('RGB', (250, 35), random_color())

    # 在该图片对象上生成一个画笔对象
    draw_obj = ImageDraw.Draw(img_obj)

    # font_obj = ImageFont.truetype('static/font/kumo.ttf', 28)

    font_obj = ImageFont.truetype(r'/usr/share/fonts/deepin-font-install/Arial/arialbi.ttf', 36)
    # font_obj = ImageFont.load_default().font
    temp = []
    for i in range(5):
        l = chr(random.randint(97, 122))  # 小写字母
        b = chr(random.randint(65, 90))  # 大写字母
        n = str(random.randint(0, 9))

        t = random.choice([l, b, n])
        temp.append(t)

        draw_obj.text((i * 40 + 35, 0), t, fill=random_color(), font=font_obj)

    # 加干扰线
    width = 250  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=random_color())

    request.session['v_code'] = ''.join(temp).upper()

    from io import BytesIO
    f1 = BytesIO()
    img_obj.save(f1, format="PNG")
    img_data = f1.getvalue()

    return HttpResponse(img_data, content_type='image/png')


# 登陆
class LoginViews(View):
    def get(self, request):
        return render(request, 'login2.html')

    def post(self, request):
        stu_name = request.POST.get('stu_name')
        stu_pwd = request.POST.get('stu_pwd')
        v_code = request.POST.get('v_code', '').upper()
        v_code_new =request.session.get('v_code')
        if v_code_new == v_code:
            # 判断checkbox 是否选中
            is_check = (request.POST.get('check_un') == 'ok')
            # 验证密码是否正确
            user_obj = auth.authenticate(request, email=stu_name, password=stu_pwd)
            if user_obj:
                print('7' * 20)
                # 把登陆用户加入
                auth.login(request, user_obj)
                permission.init(request, user_obj)
                # # 从userinfo　获取ｕｒｌ
                # # url_list = UserProfile.objects.all().values_list('role__permissions__url')
                # # 跨表查询ｕｒｌ
                # url_list = user_obj.roles.all().filter(permissions__isnull=False).values_list('permissions__url')
                # permission_list = [permission[0] for permission in url_list]
                # print(permission_list)
                # print('#'*40)
                # # 获取setting 设置的值
                # key = getattr(settings,'PERMISSION_SESSION_KEY', 'permission_url')
                # request.session[key] = permission_list
                # 判断是否选中７天免登陆
                if is_check:
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)
                next_url = reverse('crm:cus_list')
                print(next_url)
                return redirect(next_url)
            else:
                print('-' * 30)
                return render(request, 'login2.html', {"error_msg": '用户名密码错误'})
        else:

            return render(request, 'login2.html', {"error_msg": '验证码失败'})


# 注册
class RegViews(View):
    def get(self, request):
        form_obj = RegisteredForm()
        print('@' * 80)
        return render(request, 'reg.html', {"form_obj": form_obj})

    def post(self, request):

        # 实例化一个form　对象, 接受request.post
        form_obj = RegisteredForm(request.POST)

        # 创建一个ajax 验证字典
        res = {'code': 0}
        # 校验是否通过验证
        if form_obj.is_valid():
            # 清理数据　 cleaned_data() 数据里面多出了确认密码的选项，ｐｏｐ出去
            data = form_obj.cleaned_data
            data.pop("re_password")
            # 创建用户
            UserProfile.objects.create_user(**data)
            # 打入日志
            logger.info(data)
            # 规范化的地址
            next_url = reverse('crm:login')
            print(next_url)
            res['url'] = next_url
            return JsonResponse(res)
        else:
            print('&' * 80, 'new')
            res['code'] = 1
            # python json 不能传对象
            res['essor_msg'] = form_obj.errors
            return JsonResponse(res)


# ajax检查
def check_user(request):
    ''' 检测input 输入是否可靠'''
    form_obj = RegisteredForm(request.POST)
    res = {'code': 0}
    if request.method == "POST":
        # 解析　request.POST 形成一个可靠数据
        for key, val in request.POST.items():
            # 字段唯一判断
            if key in ['phone', 'email']:
                data = {key: val}
                is_user = UserProfile.objects.filter(**data)
                # print(is_user)
                # 如果is_user 存在返回错误消息
                if is_user:
                    res['code'] = 1
                    res['error_msg'] = '该选项已存在！'
                    print('!' * 80)
                    return JsonResponse(res)
            if val is None:
                print('%' * 20)
                res['code'] = 1
                res['error_msg'] = '请正确输入！'
                print('!' * 80)
                return JsonResponse(res)

    return JsonResponse(res)

# 注销


class Logout(View):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        print('+' * 20)
        if request.method == 'POST':
            from django.contrib import auth
            auth.logout(request)
            print('%' * 20)
            next_change = reverse('crm:login')
            return JsonResponse({'code': 0, 'url': next_change})

# 修改密码


class ChangeVires(View):
    def get(self, request):
        return render(request, 'change.html')


# 使用极验滑动验证码的登录

def login(request):
    # if request.is_ajax():  # 如果是AJAX请求
    print('11111')
    if request.method == "POST":
        # 初始化一个给AJAX返回的数据
        ret = {"status": 0, "msg": ""}
        # 从提交过来的数据中 取到用户名和密码
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        print(username, pwd)
        print(username, pwd)
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]

        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:
            # 验证码正确
            # 利用auth模块做用户名和密码的校验
            user = auth.authenticate(email=username, password=pwd)
            print(user, '%' * 20)
            if user:
                # 用户名密码正确
                # 给用户做登录
                auth.login(request, user)

                # 判断checkbox 是否选中
                is_check = (request.POST.get('check_un') == 'ok')
                # 判断是否选中７天免登陆
                if is_check:
                    request.session.set_expiry(7 * 24 * 60 * 60)
                else:
                    request.session.set_expiry(0)
                next_url = reverse('crm:cus_list')
                print(next_url)
                ret["msg"] = next_url
            else:
                # 用户名密码错误
                ret["status"] = 1
                ret["msg"] = "用户名或密码错误！"
        else:
            ret["status"] = 1
            ret["msg"] = "验证码错误"

        return JsonResponse(ret)
    print('%' * 20)
    return render(request, "login.html")


# 获取验证码图片的视图
def get_valid_img(request):
    # with open("valid_code.png", "rb") as f:
    #     data = f.read()
    # 自己生成一个图片
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp,
                      fill=get_random_color(), font=font_obj)

    print("".join(tmp_list))
    print("生成的验证码".center(120, "="))
    # 不能保存到全局变量
    # global VALID_CODE
    # VALID_CODE = "".join(tmp_list)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    # width = 220  # 图片宽度（防止越界）
    # height = 35
    # for i in range(5):
    #     x1 = random.randint(0, width)
    #     x2 = random.randint(0, width)
    #     y1 = random.randint(0, height)
    #     y2 = random.randint(0, height)
    #     draw_obj.line((x1, y1, x2, y2), fill=get_random_color())
    #
    # # 加干扰点
    # for i in range(40):
    #     draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
    #     x = random.randint(0, width)
    #     y = random.randint(0, height)
    #     draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 将生成的图片保存在磁盘上
    # with open("s10.png", "wb") as f:
    #     img_obj.save(f, "png")
    # # 把刚才生成的图片返回给页面
    # with open("s10.png", "rb") as f:
    #     data = f.read()

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    from io import BytesIO
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"


# 处理极验 获取验证码的视图
def get_geetest(request):
    print('&' * 20)
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)
