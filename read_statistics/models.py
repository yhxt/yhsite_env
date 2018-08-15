from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class ReadNum(models.Model):
    read_num=models.IntegerField(default=0,verbose_name='阅读数')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name='阅读数'
        verbose_name_plural=verbose_name


# 创建个阅读数继承方法ReadNumExpandMethod类
class ReadNumExpandMethod():
    # 添加方法,添加的get_read_num方法，用于在admin管理后台的blog页面显示阅读数。即在admin.py的BlogAdmin类的list_display添加read_num
    def get_read_num(self):
        # 返回该篇文章的阅读数,此处如果该文章还没有阅读数，会有个异常，该异常是的默认阅读数不是0，而是-
        try:
            ct=ContentType.objects.get_for_model(self)
            readnum=ReadNum.objects.get(content_type=ct,object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0

class ReadDetail(models.Model):
    '''阅读详情-每日阅读数'''
    date=models.DateField(default=timezone.now,verbose_name='阅读时间')
    read_num=models.IntegerField(default=0,verbose_name='阅读数')
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name='阅读详情'
        verbose_name_plural=verbose_name