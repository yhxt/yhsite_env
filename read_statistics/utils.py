import datetime
from django.utils import timezone
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import ReadNum,ReadDetail

def read_statistics_once_read(request,obj):
    ct=ContentType.objects.get_for_model(obj)
    key="%s_%s_read" % (ct.model,obj.pk)

    # 获取cookie：根据获取cookie的key值'blog_%s_readed' % blog_pk，判断是否存在，不存在则阅读数+1
    if not request.COOKIES.get(key):

        # 阅读总数+1
        readnum, created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num += 1    #点击该篇文章，阅读数自增1
        readnum.save()

        # 当天阅读数+1    
        date=timezone.now().date()
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk,date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    '''获取前7天阅读数据，根据传入类型获取相应类型前7天阅读数'''
    dates=[]         # 前7天的日期列表
    read_nums=[]     # 前7天日期的阅读数列表
    today=timezone.now().date() #当天时间
    for i in range(7,0,-1):
        # 获取前7天的数据
        date=today-datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details=ReadDetail.objects.filter(content_type=content_type,date=date)  #查询某天的阅读详情对象
        result=read_details.aggregate(read_num_sum=Sum('read_num'))  #根据read_num字段求和Sum('read_num')，并保存在read_num_sum变量中
        read_nums.append(result['read_num_sum'] or 0) #取出result中read_num_sum变量，添加到read_nums列表中,如果当天没有数据显示0
    return dates,read_nums

def get_today_hot_data(content_type):
    '''获取今天24小时阅读数量-按照阅读量从多到少排序,取前7条数据'''
    today = timezone.now().date() #当天的时间
    read_details = ReadDetail.objects.filter(content_type=content_type,date=today).order_by('-read_num')[:7]
    return read_details

def get_yesterday_hot_data(content_type):
    '''获取昨天阅读数量-按照阅读量从多到少排序,取前7条数据'''
    today = timezone.now().date()         #当天的时间
    yesterday=today-datetime.timedelta(days=1) #昨天的时间
    read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num')[:7]
    return read_details