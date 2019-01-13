from django.conf.urls import url
from app01 import views
urlpatterns = [
    url('index/', views.index, name='index'),
    url('edit/', views.edit_person, name='edit'),
    url('update/', views.update, name='update'),
]