from django.shortcuts import render,get_object_or_404
# from django.core.paginator import Paginator
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.contenttypes.models import ContentType
from django.conf import settings    #引入自定义分页显示条数
from .models import Blog_type,Blog,User



# from read_statistics.models import ReadNum
from read_statistics.utils import read_statistics_once_read

# 分页功能代码的分离
def PageNumber(request,objects_list):
    # 分类页面分页功能的实现
    try:
        page=request.GET.get('page',1)  # 获取url的页面参数(GET请求),如果没有就取第一页
    except PageNotAnInteger:
        page=1
    p=Paginator(objects_list,settings.EACH_PAGE_BLOGS_NUMBER,request=request)    # 从上面blogs获取的所有博客文章按照每页3篇的数量来分页
    blogs_page=p.page(page)
    return blogs_page


def blog_list(request):
    """博客首页列表"""
    blog_types=Blog_type.objects.all()  # 博客分类
    authors=User.objects.all()    # 作者分类
    blogs=Blog.objects.filter(is_delete=False)  # 所有博文数量(排除掉is_delete标记的软删除文章)
    blogs_nums=blogs.count()    # 总共博客数量，相当于Blog.objects.filter(is_delete=False).count()
    blogs_page=PageNumber(request,blogs)  #使用分页函数实现分页（方法二）
    dates=Blog.objects.dates('created_time','month',order='DESC')  #根据博客创建时间的月份查询博客
    return render(request,'blog/blog_list.html',{'blogs':blogs_page,'blogs_nums':blogs_nums,
                                        'blog_types':blog_types,'authors':authors,'dates':dates})


def blog_detail(request,blog_pk):
    """博客详情页"""
    blog=get_object_or_404(Blog,pk=blog_pk) # 根据传入blog_pk的ID来找到具体对应博客文章
    read_cookie_key=read_statistics_once_read(request,blog)

    pre_blog=Blog.objects.filter(id__gt=blog.id).last() # 博客的上一篇文章
    next_blog=Blog.objects.filter(id__lt=blog.id).first()   # 博客的下一篇文章

    response=render(request,'blog/blog_detail.html',{'blog':blog,'pre_blog':pre_blog,'next_blog':next_blog,
                                                     })    #响应

    # 设置cookie,打开过这篇文章即写入cookie,key是'blog_%s_readed' % blog_pk,value是'true'
    response.set_cookie(read_cookie_key,'true') #阅读cookie的标记
    return response


def blogs_with_type(request,blog_type_pk):
    """对应分类下的所有博客列表(点击分类显示该分类下的所有博客)"""
    blog_type=get_object_or_404(Blog_type,pk=blog_type_pk)  # 根据传入的ID查询出来所属分类(用于博客分类页面的title显示取值,以及分类页面分类：公司公告)
    # 再根据所属分类的id，找出此类id下面的所有博客文章
    # blogs=Blog.objects.filter(blog_type=blog_type) 另一种取值方式
    blogs=Blog.objects.filter(blog_type=blog_type_pk,is_delete=False)  #  根据所属分类的id，过滤此类id下面的所有博客文章
    blogs_nums=blogs.count()  # 该分类下的博客数量，相当于Blog.objects.filter(blog_type=blog_type_pk,is_delete=False).count()
    blog_types=Blog_type.objects.all()      # 用于获取进入分类页面的‘博客分类’显示
    authors=User.objects.all()      # 用于获取进入作者分类页面的‘作者分类’显示
    dates=Blog.objects.dates('created_time','month',order='DESC')  #用于获取进入作者分类页面的‘归档日期’显示
    blogs_page=PageNumber(request,blogs)  #使用分页函数实现分页
    return render(request,'blog/blogs_with_type.html',{'blogs':blogs_page,'blogs_nums':blogs_nums,
                                                    'blog_types':blog_types,'authors':authors,'blog_type':blog_type})



def blogs_with_author(request,blog_author_pk):
    """对应作者下的所有博客列表(点击作者显示该作者的所有博客)"""
    blog_author=get_object_or_404(User,pk=blog_author_pk)       # 根据传入的作者ID查询出来作者(用于作者分类页面title显示取值,以及作者页面的作者：谢霆锋)
    # blogs=Blog.objects.filter(author=blog_author_pk,is_delete=False)
    blogs=Blog.objects.filter(author=blog_author,is_delete=False)
    blogs_nums=blogs.count()    #用于作者页面显示数量
    blog_types=Blog_type.objects.all()  # 用于获取进入分类页面的‘博客分类’显示
    authors=User.objects.all()      # 用于获取进入作者分类页面的‘作者分类’显示
    dates=Blog.objects.dates('created_time','month',order='DESC')  #用于获取进入作者分类页面的‘归档日期’显示
    blogs_page=PageNumber(request,blogs)  #使用分页函数实现分页
    return render(request,'blog/blogs_with_author.html',{'blogs':blogs_page,'blogs_nums':blogs_nums,
                                                'blog_types':blog_types,'authors':authors,'blog_author':blog_author,'dates':dates})

def blogs_with_date(request,year,month):
    blog_time='%s年%s月' % (year,month)
    blogs=Blog.objects.filter(created_time__year=year,created_time__month=month)
    blogs_nums=blogs.count()    #用于归档日期显示数量
    blog_types=Blog_type.objects.all()  # 用于获取进入分类页面的‘博客分类’显示
    authors=User.objects.all()      # 用于获取进入作者分类页面的‘作者分类’显示
    dates=Blog.objects.dates('created_time','month',order='DESC')  #用于获取进入作者分类页面的‘归档日期’显示
    blogs_page=PageNumber(request,blogs)  #使用分页函数实现分页
    return render(request,'blog/blogs_with_date.html',{'blogs':blogs_page,'blog_time':blog_time,
                        'blogs_nums':blogs_nums,'blog_types':blog_types,'authors':authors,'dates':dates})

