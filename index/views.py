from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.shortcuts import render

# Create your views here.
from user import models1
from user.models1 import TBook, TCategory


def index(request):
    txt_username = request.session.get("username");
    cates1 = TCategory.objects.filter(level=1)
    cates2 = TCategory.objects.filter(level=2)

    new_books = TBook.objects.all().order_by('-shelf_time')[0:8]

    new_pop_books = TBook.objects.all().order_by('-sold_amount')
    li = []
    for i in range(new_pop_books.count()):
        li.append(new_pop_books[i])
    for i in range(0,len(li)-1):
        for j in range(0,i+1):
            if li[j].shelf_time < li[j+1].shelf_time:
                li[j],li[j+1] = li[j+1],li[j]

    rec_books = TBook.objects.all().order_by('-comment_amount')
    if(txt_username==None):
        return render(request,'index.html',{'li':li[:6],'cates1':cates1,'cates2':cates2,'new_books':new_books,'rec_books':rec_books})
    else:
        return render(request,'index.html',{'txt_username':txt_username,'li':li[:6],'cates1':cates1,'cates2':cates2,'new_books':new_books,'rec_books':rec_books})


def bookdetail(request):
    txt_username = request.session.get("username");
    idd = request.GET.get('id')
    book = TBook.objects.get(id=idd)
    sales = book.cur_price/book.price*10
    cate_id = book.cate_id
    cate = TCategory.objects.get(id=cate_id)
    parent_id = cate.parent_id
    p_cate = TCategory.objects.get(id=parent_id)
    return render(request,'Book details.html',{'txt_username':txt_username,'book':book,'sales':sales,'cate':cate,'p_cate':p_cate})

def booklist(request):
    txt_username = request.session.get("username");
    cates1 = TCategory.objects.filter(level=1)
    cates2 = TCategory.objects.filter(level=2)


    p_cate = request.GET.get('p_cate')
    cate = request.GET.get('cate')
    print(p_cate,12312313121)
    p_cate_name = TCategory.objects.get(id=p_cate)
    if cate != None:
        cate_name = TCategory.objects.get(id=cate)

    if cate == None:     #点的是一级标题
        print(p_cate,121212121212,type(p_cate))
        p_cate=int(p_cate)
        cate_items = TCategory.objects.filter(parent_id=p_cate)

        books = models1.TBook.objects.none()
        for c in cate_items:
            book = TBook.objects.filter(cate_id=c.id)
            if book.exists():
                books = book | books
            else:
                continue
        num = request.GET.get('num',1)
        paginator = Paginator(books,per_page=4)
        page = paginator.page(num)
        return render(request,'booklist.html',{'txt_username':txt_username,'num':num,'cates1':cates1,'cates2':cates2,'books':books,'page':page,'p_cate':p_cate,'p_cate_name':p_cate_name})

    if cate != None and p_cate != None: #点的是二级标题
        cate_items = TCategory.objects.get(id=cate)
        books = TBook.objects.filter(cate_id=cate_items)
        num = request.GET.get('num',1)
        paginator = Paginator(books,per_page=4)
        page = paginator.page(num)
        return render(request,'booklist.html',{'txt_username':txt_username,'num':num,'cates1':cates1,'cates2':cates2,'books':books,'page':page,'cate':cate,'cate_name':cate_name,'p_cate':p_cate,'p_cate_name':p_cate_name})