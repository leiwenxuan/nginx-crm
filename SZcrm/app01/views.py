from django.shortcuts import render, HttpResponse, redirect
from app01.models import Person
from app01.forms import Personform
from django.urls import reverse
from crm.models import UserProfile

from SZcrm import settings
from django.http import JsonResponse
# Create your views here.


def index(request):
    person_list = Person.objects.all()
    return render(request, 'app01/index.html', {'person_list': person_list})

def edit_person(request):
    # 1-3 获取get 请求id 获取表对象，　实例一个ｆｏｒｍ 对象
    edit_id = request.GET.get('id')
    person_obj = Person.objects.filter(id=edit_id).first()
    form_obj = Personform(instance=person_obj)
    print(edit_id)
    if request.method == 'POST':
        form_obj = Personform(request.POST, instance=person_obj)
        if form_obj.is_valid():
            # 自动修改
            form_obj.save()
            return redirect(reverse('app01:index'))
        else:
            print('2'*10)
            return render(request, 'app01/edit_person.html', {'form_obj': form_obj, 'error_msg': '不符合要求'})


    return render(request, 'app01/edit_person.html', {'form_obj': form_obj})


import xlrd
def update(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('filename')
        print(file_obj.name,len(file_obj))
        # print(len(file_obj))
        # with open(file_obj.name, 'wb') as f:
        #     for i in file_obj:
        #         f.write(i)
        # print('#'*120)
        workbook = xlrd.open_workbook(file_contents=file_obj.file.read())
        print(workbook)
        # 工作表一
        row_map = {
            0: {
                'text': '邮件',
                'name': 'email'
            },
            1: {
                'text': '姓名',
                'name': 'name'
            },
            2: {
                'text': '密码',
                'name': 'password'
            },

        }
        sheet = workbook.sheet_by_index(0)
        print(sheet)
        object_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)
            row_dict = {}
            for col_num, name_text in row_map.items():
                row_dict[name_text['name']] = row[col_num].value
            print(row_dict)
            UserProfile.objects.create_user(**row_dict)

        return HttpResponse('OK')
    return render(request, 'app01/downup.html')





