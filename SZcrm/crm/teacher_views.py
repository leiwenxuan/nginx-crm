from django.forms import modelformset_factory
from django import views
from crm.models import ClassList, ConsultRecord, CourseRecord, StudyRecord
from django.shortcuts import render, redirect, HttpResponse
from crm.forms import ClassForms, CourseRecordForm, StudyRecordForm
from django.urls import reverse
from django.http import QueryDict


# 班级列表
class ClasslistViews(views.View):
    def get(self, request):
        query_set = ClassList.objects.all()

        return render(request, 'class_list.html', {'class_list': query_set})

    def post(self, request):
        return HttpResponse("班级列表 post")


# 添加和编辑班级
def add_list(request, eidt_id=0):
    class_obj = ClassList.objects.filter(id=eidt_id).first()
    form_obj = ClassForms(instance=class_obj)
    if request.method == 'POST':
        form_obj = ClassForms(request.POST, instance=class_obj)
        if form_obj:
            form_obj.save()
            return redirect(reverse('crm:class_list'))
        else:
            return render(request, 'add_class.html', {"form_obj": form_obj})
    print(eidt_id)
    return render(request, 'add_class.html', {
        "form_obj": form_obj,
        'eidt_id': eidt_id
    })


# 课程记录 列表
class CourseRecordviews(views.View):
    def get(self, request, class_id=0):
        # 根据班级id 查询出所有的上课记录
        consult_obj = CourseRecord.objects.filter(re_class_id=class_id)
        print(consult_obj)
        # 获取url参数， 拼接起来
        current_url = request.get_full_path()
        qd = QueryDict(mutable=True)
        qd['next'] = current_url
        next_ulr = qd.urlencode()
        seed_data = {
            "consult_obj": consult_obj,  # 传送数据大字典
            "next_url": next_ulr,  # url
            "class_id": class_id,
        }
        return render(request, 'course_list.html', seed_data)

    def post(self, request, class_id):
        # 1.处理从POST 提交过来的数据找到action 和勾选的课程id
        cid = request.POST.getlist('cid')
        print(request.POST)
        action = request.POST.get('action')
        print(cid, action, "&" * 80)
        # 2 反射批量处理数据
        if hasattr(self, '_{}'.format(action)):
            ret = getattr(self, '_{}'.format(action))(cid)
        else:
            return HttpResponse("此选择无效")

        if ret:
            return ret
        else:
            return redirect(
                reverse('crm:courserecord', kwargs={'class_id': class_id}))

    # 类私有方法： 功能批量生成课程记录表
    def _multi_init(self, cid):
        # 课程id在cid里面的才进行创建
        courser_obj = CourseRecord.objects.filter(id__in=cid)

        # 业务分析， 应该每一课时创建一条记录
        # courser_obj 这是多个课程的列表循环批量处理
        for course_record in courser_obj:
            # 根据课程表反向查找 学生
            all_student = course_record.re_class.customer_set.all()
            studentreord_objs = (StudyRecord(
                course_record=course_record, student=student)
                                 for student in all_student)
            StudyRecord.objects.bulk_create(studentreord_objs)
        return HttpResponse("初始化好了")


# 添加课程记录表
class AddCourseViews(views.View):
    def get(self, request, class_id=0, course_record_id=None):
        # 查找班级对象，
        class_obj = ClassList.objects.filter(id=class_id).first()
        # 要修改的对象
        edit_obj = CourseRecord.objects.filter(id=course_record_id).first()
        form_obj = CourseRecordForm(
            instance=edit_obj, initial={'re_class': class_obj})
        seed_data = {'form_obj': form_obj, 'edit_id': course_record_id}
        return render(request, 'add_course.html', seed_data)

    def post(self, request, class_id=0, course_record_id=None):
        edit_obj = CourseRecord.objects.filter(id=course_record_id).first()
        # 实例化对象
        form_obj = CourseRecordForm(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            next_url = request.GET.get('next', '/crm/class_list/')
            return redirect(next_url)
        seed_data = {
            'form_obj': form_obj,
        }
        return render(request, 'add_course.html', seed_data)


# 学习记录列表
def student_list(request, course_record_id):
    '''
    modelformset_factory: 用法
        １. views视图　 modelformset_factory(StudyRecord, StudyRecordForm, extra=0)
        ２．拿到实例化的类　实例化自己要生成的ｆｏｒｍ表单　
        ３．post －－> formSet(request.POST, queryset=query_set) 和formmodel 类似
        4. formset_obj.is_valid(): 成功保存，　否则报错
    需要注意的：
    １．模板界面必须有　 {{ formset.management_form }}
    ２．循环　要有form.id
    3. 生成form的字段 和提交的form 字段必须对应，　否则验证失败，因为不匹配
    :param request:
    :param course_record_id: 课程记录的id　没门课程可以找到，当前课程的所有学生
    :return:
    '''

    # form 内置函数接收一个model对象， 一个modelForm 对象
    # extea 取消默认的一个空表格, 返回一个类
    formSet = modelformset_factory(StudyRecord, StudyRecordForm, extra=0)
    # 根据课程记录的id 找到这个班级下所有的学生course_record_id=course_record_id
    query_set = StudyRecord.objects.filter(course_record_id=course_record_id)
    # 拿到上面函数的返回类实例化, 实例化一个fomr表格
    formset_obj = formSet(queryset=query_set)
    if request.method == 'POST':
        # 实例话一个form对象
        print('post' * 5)
        formset_obj = formSet(request.POST, queryset=query_set)
        print(formset_obj.is_valid())
        if formset_obj.is_valid():
            print('保存了吗')
            formset_obj.save()
    return render(request, 'student_list.html', {'formset': formset_obj})
