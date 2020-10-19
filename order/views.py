from MySQLdb import Date
from django.core.serializers import json
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


# Create your views here.
from django.utils import timezone

from car.tests import Book
from user.models1 import TItems, TBook, TAddress, TOrder, TUser

def addr(request):
    txt_username = request.session.get("username");
    if txt_username != None:
        user = TUser.objects.filter(username=txt_username)[0];
    if txt_username:    #如果用户已经登录
        addr_id = request.POST.get("addr_id")
        if addr_id != 'new_address':
            speciaddr = TAddress.objects.filter(id=addr_id)[0]
            dict = {'name':speciaddr.name,'cellphone':speciaddr.cellphone,'detail_address':speciaddr.detail_address,'post_code':speciaddr.post_code,'telephone':speciaddr.telephone}
            return JsonResponse(dict,safe=True)
        else:
            return HttpResponse('no')

def toindent(request):
    txt_username = request.session.get("username");
    if txt_username != None:
        user = TUser.objects.filter(username=txt_username)[0];
    if txt_username:    #如果用户已经登录
        addr_id = request.POST.get("addr_id")
        if addr_id != None:
            speciaddr = TAddress.objects.filter(id=addr_id)[0]
        car = request.session.get('car')
        addrs = TAddress.objects.filter(user_id=user.id)
        books = TItems.objects.filter(user_id=user.id)
        ids = []
        amount = []
        objs = []
        for b in books:
            ids.append(b.book_id)
            amount.append(b.book_amount)
        for idx,book in enumerate(books):
            book_obj = Book(book.book_id,book.book_amount)
            book_obj.totalprice = float(book_obj.price) * float(book_obj.count)
            objs.append(book_obj)
        if objs:     #book_list里边有数据
            total = round(0.0,2)
            for b in objs:
                total += b.totalprice
        if addr_id != None:
            dict = {'name':speciaddr.name,'cellphone':speciaddr.cellphone,'detail_address':speciaddr.detail_address,'post_code':speciaddr.post_code,'telephone':speciaddr.telephone}
            return render(request,'indent.html',{'txt_username':txt_username,'book_list':objs,'total':total,'addrs':addrs,'speciaddr':dict})
        else:
            return render(request,'indent.html',{'txt_username':txt_username,'book_list':objs,'total':total,'addrs':addrs})
        # return render(request,'indent.html',{'txt_username':txt_username,'book_list':bookItems,'total':total})
    else:     #用户没有登录
        return redirect('/tologin/')

def makeorder(request):
    txt_username = request.session.get("username")
    user = TUser.objects.filter(username=txt_username)[0]
    if request.method == 'GET':
        check1 = request.GET.get("check1")
        check2 = request.GET.get("check2")
        check3 = request.GET.get("check3")
        check4 = request.GET.get("check4")
        total = request.GET.get("total")
        ship_man = request.GET.get("ship_man")
        ship_addr = request.GET.get("ship_addr")
        ship_mail = request.GET.get("ship_mail")
        ship_cellphone = request.GET.get("ship_cellphone")
        ship_phone = request.GET.get("ship_phone")

        if(check1=='1' and check2=='1' and check3=='1' and check4=='1'):
            if ship_cellphone != None and ship_phone != None:
                res = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                if res == None:
                    with transaction.atomic():
                        TAddress.objects.create(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        ress = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=ress.id,total_price=total,create_time=timezone.now())
                        return HttpResponse('ok')
                else:
                    TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=res.id,total_price=total,create_time=timezone.now())
                    return HttpResponse('ok')
            elif ship_cellphone != None and ship_phone == None:
                res = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,user_id=user.id)
                if res == None:
                    with transaction.atomic():
                        TAddress.objects.create(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,user_id=user.id)
                        ress = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,user_id=user.id)
                        TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=ress.id,total_price=total,create_time=timezone.now())
                        return HttpResponse('ok')
                else:
                    TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=res.id,total_price=total,create_time=timezone.now())
                    return HttpResponse('ok')
            elif ship_cellphone == None and ship_phone != None:
                res = TAddress.objects.filter(name=ship_man,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                if res == None:
                    with transaction.atomic():
                        TAddress.objects.create(name=ship_man,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        ress = TAddress.objects.filter(name=ship_man,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=ress.id,total_price=total,create_time=timezone.now())
                        return HttpResponse('ok')
                else:
                    TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=res.id,total_price=total,create_time=timezone.now())
                    return HttpResponse('ok')
        else:
            return HttpResponse('no')
    else:
        check1 = request.POST.get("check1")
        check2 = request.POST.get("check2")
        check3 = request.POST.get("check3")
        check4 = request.POST.get("check4")
        total = request.POST.get("total")
        ship_man = request.POST.get("ship_man")
        ship_addr = request.POST.get("ship_addr")
        ship_mail = request.POST.get("ship_mail")
        ship_cellphone = request.POST.get("ship_cellphone")
        ship_phone = request.POST.get("ship_phone")

        if(check1=='1' and check2=='1' and check3=='1' and check4=='1'):
            if ship_cellphone != '' and ship_phone != '':
                res = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                if not res.exists():
                    with transaction.atomic():
                        TAddress.objects.create(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        ress = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=ress[0].id,total_price=total,create_time=timezone.now())
                        return HttpResponse('ok')
                else:
                    TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=res[0].id,total_price=total,create_time=timezone.now())
                    return HttpResponse('ok')
            elif ship_cellphone != '' and ship_phone == '':
                res = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,user_id=user.id)
                if not res.exists():
                    with transaction.atomic():
                        TAddress.objects.create(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,user_id=user.id)
                        ress = TAddress.objects.filter(name=ship_man,cellphone=ship_cellphone,detail_address=ship_addr,post_code=ship_mail,user_id=user.id)
                        TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=ress[0].id,total_price=total,create_time=timezone.now())
                        return HttpResponse('ok')
                else:
                    TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=res[0].id,total_price=total,create_time=timezone.now())
                    return HttpResponse('ok')
            elif ship_cellphone == '' and ship_phone != '':
                res = TAddress.objects.filter(name=ship_man,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                if not res.exists():
                    with transaction.atomic():
                        TAddress.objects.create(name=ship_man,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        ress = TAddress.objects.filter(name=ship_man,detail_address=ship_addr,post_code=ship_mail,telephone=ship_phone,user_id=user.id)
                        TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=ress[0].id,total_price=total,create_time=timezone.now())
                        return HttpResponse('ok')
                else:
                    TOrder.objects.create(order_id=5151,user_id=user.id,addr_id=res[0].id,total_price=total,create_time=timezone.now())
                    return HttpResponse('ok')
        else:
            return HttpResponse('no')



def orderok(request):
    total1 = request.GET.get('total')
    print(total1,1222222222222222222222)
    txt_username = request.session.get("username");
    user = TUser.objects.filter(username=txt_username)[0];
    order = TOrder.objects.filter(user_id=user.id)[0]
    return render(request,'indent ok.html',{'txt_username':txt_username,'order':order,'total':total1})






