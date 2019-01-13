import xlrd
from django.shortcuts import render, redirect
def customer_import(request):
    """
    批量导入
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'customer_import.html')

    context = {'status': True, 'msg': '导入成功'}
    try:
        customer_excel = request.FILES.get('customer_excel')
        """
        打开上传的Excel文件，并读取内容
        注：打开本地文件时，可以使用：workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')
        """
        workbook = xlrd.open_workbook(file_contents=customer_excel.file.read())

        # sheet = workbook.sheet_by_name('工作表1')
        sheet = workbook.sheet_by_index(0)
        row_map = {
            0: {
                'text': '客户姓名',
                'name': 'name'
            },
            1: {
                'text': '年龄',
                'name': 'age'
            },
            2: {
                'text': '邮箱',
                'name': 'email'
            },
            3: {
                'text': '公司',
                'name': 'company'
            },
        }
        object_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)
            row_dict = {}
            for col_num, name_text in row_map.items():
                row_dict[name_text['name']] = row[col_num].value
            object_list.append(models.Customer(**row_dict))

        models.Customer.objects.bulk_create(object_list, batch_size=20)
    except Exception as e:
        context['status'] = False
        context['msg'] = '导入失败'

    return render(request, 'customer_import.html', context)
