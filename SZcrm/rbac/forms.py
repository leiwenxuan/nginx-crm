from django import forms
from rbac import models
from rbac.utils import fontawesome
from django.utils.safestring import mark_safe

ICON_CHOICES = fontawesome.ICON_CHOICES


class BootStrapclass(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 给实例加样式
        for filed in self.fields.values():
            filed.widget.attrs.update({'class': 'form-control'})


class RoleForm(BootStrapclass):
    class Meta:
        model = models.Role
        fields = '__all__'


class MenuForm(BootStrapclass):
    class Meta:
        model = models.Menu
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 把icon图标这个字段由input框变成单选框
        self.fields['icon'] = forms.ChoiceField(
            widget=forms.widgets.RadioSelect,
            choices=((i[0], mark_safe(i[1])) for i in ICON_CHOICES))


class UserpurviewForm(BootStrapclass):
    class Meta:
        model = models.Userpurview
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
