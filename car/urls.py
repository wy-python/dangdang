from django.urls import path

from car import views

app_name = 'car'
urlpatterns = [
    path('carr/',views.carr,name='carr'),
    path('addcar/',views.addcar,name='addcar'),
    path('delcar/',views.delcar,name='delcar'),
    path('goods_count/',views.goods_count,name='goods_count'),
    path('raddcar/',views.raddcar,name='raddcar'),
    path('rgoods_count/',views.rgoods_count,name='rgoods_count'),
    path('rdelcar/',views.rdelcar,name='rdelcar'),

]