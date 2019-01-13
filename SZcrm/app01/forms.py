from django import forms
from app01.models import Person
from django.core.exceptions import ValidationError


class Personform(forms.ModelForm):

    class Meta:
        model = Person
        fields = "__all__"

        error_msg = {
            'name':  {'max-length':'超过限定'},
        }
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age > 90:
            raise ValidationError('你能活到那时候吗')
        else:
            return self.age