import datetime
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render,redirect
from django.core.cache import cache #缓存
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data,get_today_hot_data,get_yesterday_hot_data
from blog.models import Blog


def get_7_days_hot_blogs():
    '''获取7天内的热门阅读'''
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id','title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')[:7]
    return blogs

def home(request):
    blog_content_type=ContentType.objects.get_for_model(Blog)       # 获取文件类型
    dates,read_nums=get_seven_days_read_data(blog_content_type)     # 获取该文件类型下前7天的阅读数

    # 获取7天热门博客的缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if hot_blogs_for_7_days is None:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)
        print('cache')
    else:
        print('use cache')

    # 获取首页热门阅读
    today_hot_data = get_today_hot_data(blog_content_type)          # 获取今日24小时热门阅读点击
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)  # 获取昨天热门阅读点击
    hot_blogs_for_7_days = hot_blogs_for_7_days                 #获取7天内热门阅读点击

    return render(request,'home.html',{'dates':dates,'read_nums':read_nums,
                                                'today_hot_data':today_hot_data,
                                                'yesterday_hot_data':yesterday_hot_data,
                                                'hot_blogs_for_7_days':hot_blogs_for_7_days})


