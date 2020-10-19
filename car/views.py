from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render
from car.tests import Car, Book
from user.models1 import TItems,TUser


def carr(request):
    txt_username = request.session.get('username')
    if txt_username != None:
        user = TUser.objects.filter(username=txt_username)[0]
    if txt_username == None:     #没有登录的情况下
        car = request.session.get("car")
        if car != None:     #如果购物车不为空
            book_list = car.get_list()
            if book_list:    #如果购物车中有书
                total = round(0.0,2)
                for b in book_list:
                    total += b.totalprice
                return render(request,'car.html',{'txt_username':txt_username,'car':car,'book_list':book_list,'total':total});
            else:          #如果购物车中没书
                return render(request,'car.html',{'txt_username':txt_username,'car':car});
        else:     #购物车为空，去逛逛
            return render(request,'car.html',{'txt_username':txt_username});

    else:     #已经登录的情况下

        car = request.session.get("car")
        books = TItems.objects.filter(user_id=user.id)
        if books != None:
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
            if objs:     #book_list里边有数据，将session中的数据移到表中，并清空session
                total = round(0.0,2)
                for b in objs:
                    total += b.totalprice
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
                car = 1
                return render(request,'car.html',{'txt_username':txt_username,'car':car,'book_list':objs,"total":total})
            else:        #登录状态下，把session中的数据加入到数据库中
                if car:
                    book_list = car.get_list()
                    for b in book_list:
                        b.totalprice = float(b.price) * float(b.count)
                        TItems.objects.create(order_id=1,user_id=user.id,book_id=b.id,book_amount=b.count)
                    total = 0
                    for b in book_list:
                        total += b.totalprice
                    request.session['car'] = car
                    return render(request,'car.html',{'txt_username':txt_username,'car':car,'book_list':book_list,'total':total})
                else:
                    return render(request,'car.html',{'txt_username':txt_username})
                # book_list = TItems.objects.all()
                # return render(request,'car.html',{'txt_username':txt_username,'book_list':book_list})
        # else:               #购物车为空，去逛逛
            return render(request,'car.html',{'txt_username':txt_username})


def addcar(request):
    book_id = request.POST.get('book_id')
    #构建好后调用方法将书存进去即可
    car = request.session.get('car')
    count = request.POST.get("count")
    if car:
        car.add_book(book_id,int(count))
        request.session['car'] = car
        return HttpResponse('ok')
    else:
        car = Car()
        car.add_book(book_id,int(count))
        request.session['car'] = car
        if request.session.get('car'):
            return HttpResponse('ok')
        return HttpResponse('no')

def delcar(request):
    book_id = request.POST.get("book_id")
    car = request.session.get("car")
    car.remove_book(book_id)
    request.session['car'] = car
    return HttpResponse('ok')


def goods_count(request):
    id = request.POST.get("book_id")
    count = request.POST.get("count")
    total = 0
    car = request.session.get("car")
    for book in car.book_list:
        if book.id == id:
            book.count = int(count)
            total = book.count * book.price
            book.totalprice = total
    request.session['car'] = car
    return HttpResponse(round(float(total),2))

# 登陆后的函数
def raddcar(request):
    book_id = request.POST.get('book_id')
    #构建好后调用方法将书存进去即可
    count = request.POST.get("count")
    car = request.session.get('car')
    txt_username = request.session.get("username")
    user = TUser.objects.filter(username=txt_username)[0]
    if car:
        car.add_book(book_id,int(count))
        book_list = car.get_list()
        for b in book_list:
            b_id = b.id
            res = TItems.objects.filter(book_id=b_id)
        if res:    #已经有了这本书，要改数量
            preamount = int(res[0].book_amount)
            res[0].book_amount = int(count) + int(preamount)
            res[0].save()
            request.session['car'] = car
            flag = 1
        else:
            TItems.objects.create(order_id=1,user_id=user.id,book_id=b.id,book_amount=b.count)
            request.session['car'] = car
            flag = 1
        if flag == 1:
            return HttpResponse("ok")
        return HttpResponse("no")

    else:    #car还没有
        car = Car()
        car.add_book(book_id,int(count))
        book_list = car.get_list()
        for b in book_list:
            TItems.objects.create(order_id=1,user_id=user.id,book_id=b.id,book_amount=b.count)
            flag = 1
            request.session['car'] = car
        if flag == 1:
            return HttpResponse("ok")
        return HttpResponse("no")

def rdelcar(request):
    book_id = request.POST.get("book_id")
    with transaction.atomic():
        book = TItems.objects.filter(book_id=book_id).delete()
    return HttpResponse('ok')

def rgoods_count(request):
    id = request.POST.get("book_id")
    count = request.POST.get("count")
    total = 0
    book = TItems.objects.filter(book_id=id)[0]
    book.book_amount = int(count)
    book.save()
    book_obj = Book(int(id),int(count))
    total = float(book_obj.count) * float(book_obj.price)
    book_obj.totalprice = total
    return HttpResponse(round(float(total),2))

