# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class TAddress(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20, blank=True, null=True)
    cellphone = models.CharField(max_length=11, blank=True, null=True)
    detail_address = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=6, blank=True, null=True)
    telephone = models.CharField(max_length=10, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_address'


class TBook(models.Model):
    id = models.IntegerField(primary_key=True)
    book_pic = models.CharField(max_length=100, blank=True, null=True)
    book_title = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(max_length=100, blank=True, null=True)
    shelf_time = models.DateTimeField(blank=True, null=True)
    published_time = models.DateTimeField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    cur_price = models.FloatField(blank=True, null=True)
    comment_amount = models.IntegerField(blank=True, null=True)
    sold_amount = models.IntegerField(blank=True, null=True)
    repertory = models.IntegerField(blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    printed_time = models.DateTimeField(blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    printed_frequency = models.IntegerField(blank=True, null=True)
    edition = models.IntegerField(blank=True, null=True)
    page_number = models.IntegerField(blank=True, null=True)
    page_size = models.IntegerField(blank=True, null=True)
    package = models.CharField(max_length=20, blank=True, null=True)
    char_amount = models.CharField(max_length=20, blank=True, null=True)
    paper_category = models.CharField(max_length=20, blank=True, null=True)
    editor_rcmd = models.TextField(blank=True, null=True)
    content_rcmd = models.TextField(blank=True, null=True)
    author_intro = models.TextField(blank=True, null=True)
    catalog = models.TextField(blank=True, null=True)
    media_comment = models.TextField(blank=True, null=True)
    section = models.TextField(blank=True, null=True)
    cate = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_book'

    def getsale(self):
        return "%.2f"%float(float(self.cur_price)/float(self.price)*10)


class TCar(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_car'


class TCategory(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    level = models.IntegerField(blank=True, null=True)
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_category'


class TItems(models.Model):
    order = models.ForeignKey('TOrder', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)
    book_amount = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_items'


class TOrder(models.Model):
    id = models.IntegerField(primary_key=True)
    order_id = models.CharField(max_length=20, blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    addr = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_order'


class TUser(models.Model):
    username = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 't_user'
