from django.urls import path

from order import views

app_name = 'index'
urlpatterns = [
    path('toindent/',views.toindent,name='toindent'),
    path('makeorder/',views.makeorder,name='makeorder'),
    path('orderok/',views.orderok,name='orderok'),
    path('addr/',views.addr,name='addr'),

]