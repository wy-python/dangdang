from django.test import TestCase

# Create your tests here.
from user.models1 import TBook

#一个简化版的book，从TBook中来
class Book:
    def __init__(self,id,count):
        book = TBook.objects.get(id=id) #获取到这个Book对象
        self.id = id
        self.title = book.book_title
        self.count = count
        self.price = book.cur_price
        self.picture = book.book_pic
        self.totalprice = book.cur_price

class Car:
    def __init__(self):
        self.book_list = []

    def get_book(self,id):
        for book in self.book_list:
            if book.id == id:
                return book
        return None

    def add_book(self,id,count=1):#增加书的时候要先判断购物车中有没有这本书
        book = self.get_book(id)
        if book:         #如果已经有了，修改书的数量即可
            book.count += int(count)
            book.totalprice += float(book.price) * float(count)
        else:            #如果没有，则需要给购物车添加这本书的信息
            book = Book(id=id,count=count)
            book.count = int(count)
            book.totalprice = float(book.price) * float(count)
            self.book_list.append(book)


    def remove_book(self,id):
        book = self.get_book(id)
        print('...remove',book)
        self.book_list.remove(book)


    def get_list(self):
        return self.book_list


