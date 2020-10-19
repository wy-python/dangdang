from django.urls import path

from user import views

app_name = 'user'
urlpatterns = [
    path('toregister/',views.toregister,name='toregister'),
    path('register/',views.register,name='register'),
    path('captcha/',views.captcha,name='captcha'),
    path('checkname/',views.checkname,name='checkname'),
    path('checkvcode/',views.checkvcode,name='checkvcode'),
    path('register/',views.register,name='register'),
    path('registerok/',views.registerok,name='registerok'),
    path('tologin/',views.tologin,name='tologin'),
    path('lcheckname/',views.lcheckname,name='lcheckname'),
    path('lcheckpassword/',views.lcheckpassword,name='lcheckpassword'),
    path('lcheckvcode/',views.lcheckvcode,name='lcheckvcode'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),

]