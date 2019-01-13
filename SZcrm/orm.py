import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SZcrm.settings")
    import django
    django.setup()
    from crm.models import Customer

    # pub_list = (Publisher(name='南山{}'.format(i)) for i in range(100, 1000))
    # Publisher.objects.bulk_create(pub_list, 10)
    # #
    # # ret = Publisher.objects.all()
    # # print(ret)Golang高级开发
    # pub_list = Publisher.objects.all().count()
    # print(pub_list)

    customer = (Customer(qq='8920286{}'.format(i), qq_name='深圳{}'.format(i), name='无言{}'.format(i),
                         course='Golang高级开发',
                         ) for i in range(0,30))
    Customer.objects.bulk_create(customer,10)

    # from app01.models import Person
    # person_list = (Person(name='无言{}'.format(i),
    #                       age='{}'.format(i), hobby='读书{}'.format(i) )for i  in range(10))
    #
    # Person.objects.bulk_create(person_list, 10)
    s = '{1}'.format(7, 1)
    print(s)
