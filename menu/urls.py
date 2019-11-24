from django.conf.urls import url
from django.urls import path

from menu.views import CreateNewMenuFormView
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    url(r'^menu/(?P<pk>\d+)/edit/$', views.edit_menu, name='menu_edit'),
    url(r'^menu/(?P<pk>\d+)/$', views.menu_detail, name='menu_detail'),
    url(r'^menu/item/(?P<pk>\d+)/$', views.item_detail, name='item_detail'),
    path('menu/new/', CreateNewMenuFormView.as_view(), name='menu_new'),
]
