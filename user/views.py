import string
import random

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from user.captcha.image import ImageCaptcha
from user.models1 import TUser


def toregister(request):
    return render(request,'register.html')

def captcha(request):
    code = random.sample(string.ascii_lowercase+string.ascii_uppercase+string.digits,4)
    codes = ''.join(code)
    img = ImageCaptcha()
    data = img.generate(codes)
    request.session['code'] = codes
    print(codes,'这里是验证码')
    return HttpResponse(data,'image/png')

def checkname(request):
    if request.method == 'GET':
        txt_username = request.GET.get("txt_username")
    else:
        txt_username = request.POST.get("txt_username")
    res = TUser.objects.filter(username=txt_username)
    if res:
        return HttpResponse("已经注册过")
    else:
        return HttpResponse("ok")

def checkvcode(request):
    if request.method == 'GET':
        txt_vcode = request.GET.get("txt_vcode")
    else:
        txt_vcode = request.POST.get("txt_vcode")
    real_vcode = request.session.get('code')
    if(real_vcode.lower() != txt_vcode.lower()):
        return HttpResponse("no")
    else:
        return HttpResponse("ok")

def registerok(request):
    if request.method == 'GET':
        txt_username = request.session.get("username")
    else:
        txt_username = request.session.get("username")
    return render(request,'register ok.html',{'txt_username':txt_username})


def register(request):
    if request.method == 'GET':
        check1 = request.GET.get("check1")
        check2 = request.GET.get("check2")
        check3 = request.GET.get("check3")
        chb_agreement = request.GET.get("chb_agreement")
        if(check1=='1' and check2=='1'and check3=='1'and chb_agreement=='true'):
            with transaction.atomic():
                txt_username = request.GET.get("txt_username")
                txt_repassword = request.GET.get("txt_repassword")
                TUser.objects.create(username=txt_username,password=txt_repassword)
                # request.session['username']=txt_username
                return HttpResponse("fine")
        else:
            return HttpResponse("no")
    else:
        check1 = request.POST.get("check1")
        check2 = request.POST.get("check2")
        check3 = request.POST.get("check3")
        chb_agreement = request.POST.get("chb_agreement")
        if(check1=='1' and check2=='1'and check3=='1'and chb_agreement=='true'):
            with transaction.atomic():
                txt_username = request.POST.get("txt_username")
                txt_repassword = request.POST.get("txt_repassword")
                TUser.objects.create(username=txt_username,password=txt_repassword)
                request.session['username']=txt_username
            return HttpResponse("fine")
        else:
            return HttpResponse("no")


def tologin(request):
    url = request.GET.get("url");
    cate = request.GET.get("cate")
    if cate:
        url1 = url
        url2 = '&cate='+str(cate)
        url = url1 + url2
    return render(request,'login.html',{'url':url})

def lcheckname(request):
    txt_username = request.POST.get("txt_username")
    res = TUser.objects.filter(username=txt_username)
    if res:
        return HttpResponse("ok")
    else:
        return HttpResponse("no")

def lcheckpassword(request):
    txt_username = request.POST.get("txt_username")
    txt_password = request.POST.get("txt_password")
    res = TUser.objects.filter(username=txt_username,password=txt_password)
    if res:
        return HttpResponse("ok")
    else:
        return HttpResponse("no")

def lcheckvcode(request):
    txt_vcode = request.POST.get("txt_vcode")
    real_vcode = request.session.get('code')
    if(real_vcode.lower() != txt_vcode.lower()):
        return HttpResponse("no")
    else:
        return HttpResponse("ok")

def login(request):
    check1 = request.POST.get("check1")
    check2 = request.POST.get("check2")
    check3 = request.POST.get("check3")
    autologin = request.POST.get("autologin")
    txt_username = request.POST.get("txt_username")
    txt_password = request.POST.get("txt_password")
    if(check1=='1' and check2=='1'and check3=='1'):
        if(autologin == 'true'):
            res = render(request,'index.html')
            res.set_cookie("username",txt_username,max_age=3600*24*7)
            res.set_cookie("password",txt_password,max_age=3600*24*7)
            request.session['username']=txt_username
            return HttpResponse("fine")
        else:
            request.session['username']=txt_username
            return HttpResponse("fine")
    else:
        return HttpResponse("no")

def logout(request):
    request.session.clear()
    return redirect('/index/')
