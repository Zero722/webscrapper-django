from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<str:fname>/',views.details, name='details'),
    path('upload/',views.upload_page, name='upload'),
    path('upload_both/',views.upload_both_page, name='upload_both'),

    path('upload_json/',views.uploadjson, name='uploadjson'),
    path('upload_csv/',views.uploadcsv, name='uploadcsv'),
    path('upload_csv_json/',views.upload_csv_json, name='upload_csv_json'),


    path('list_config/',views.list_config, name='list_config'),
    path('view_config/<str:scheme_name>/',views.view_config, name='view_config'),
    path('config/edit/<str:scheme_name>/',views.edit_config, name='edit_config'),
    path('scheme/edit/',views.edit_scheme, name='edit_scheme'),

]