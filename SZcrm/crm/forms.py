"""
    这是一个自己实现form表单的注册文件
    1. 用户名 name
    2. 密码　password
    3. 确认密码　re_password
    4. 手机号　mobile
    5. 邮箱 email
"""
from django import forms
from crm import models
from django.forms.utils import ValidationError
from crm.models import UserProfile, Customer, ConsultRecord, Enrollment, ClassList, StudyRecord, CourseRecord, PaymentRecord


class Bootstrapclass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给没个实例加入样式
        for filed in self.fields.values():
            filed.widget.attrs.update({"class": 'form-control'})


class RegisteredForm(Bootstrapclass):

    re_password = forms.CharField(
        label='确认密码',
        widget=forms.widgets.PasswordInput(),
    )

    # 配置 与UserProfile　关联
    class Meta:
        model = models.UserProfile  # 关联UserProfile
        fields = ['email', 'name', 'password', 're_password', 'mobile']

        widgets = {
            'password': forms.widgets.PasswordInput(),
            're_password': forms.widgets.PasswordInput()
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_emial = UserProfile.objects.filter(email=email)
        if is_emial:
            raise ValidationError('邮箱已被注册')
        else:
            return email

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if re_password == password:
            return self.cleaned_data
        else:
            self.add_error('re_password', '两次输入密码不正确!')
            raise ValidationError('两次输入密码不正确！')


class Addfrom(Bootstrapclass):
    class Meta:
        model = Customer

        fields = '__all__'
        widgets = {
            'course': forms.widgets.SelectMultiple,
            'birthday': forms.widgets.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给没个实例加入样式

        for filed in self.fields.values():
            filed.widget.attrs.update({"class": 'form-control'})

        try:
            self.fields['consultant'].choices = [
                (self.instance.consultant.id, self.instance.consultant.name),
            ]
        except Exception as e:
            print('%' * 20)


class RecordForms(Bootstrapclass):
    class Meta:
        model = ConsultRecord
        # fields = '__all__'
        exclude = [
            'delete_status',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'] = forms.models.ModelChoiceField(
            queryset=Customer.objects.filter(
                consultant=self.instance.consultant))
        print(self.fields)
        self.fields['customer'].widget.attrs.update({'class': 'form-control'})

        self.fields['consultant'].choices = [
            (self.instance.consultant.id, self.instance.consultant.name),
        ]


# 报名表
class EnrollmentForms(Bootstrapclass):
    class Meta:
        model = Enrollment
        # fields = "__all__"
        exclude = ['contract_approved', 'delete_status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.instance.customer.name)
        self.fields['customer'].choices = [(self.instance.customer.id,
                                            self.instance.customer.name)]

        # self.fields['customer'].choices = [(self.instance.customer.id, self.instance.customer.name),]


# 班级列表form
class ClassForms(Bootstrapclass):
    class Meta:
        model = ClassList
        fields = "__all__"


# 学生列表
class StudyRecordForm(Bootstrapclass):
    class Meta:
        model = StudyRecord
        # fields = '__all__'
        fields = ('student', 'attendance', 'score', 'homework')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)


# 课程记录表
class CourseRecordForm(Bootstrapclass):
    class Meta:
        model = CourseRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class PaymentRecordForm(Bootstrapclass):
    class Meta:
        model = PaymentRecord
        fields = '__all__'
