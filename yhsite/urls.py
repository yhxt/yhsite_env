from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from yhsite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),   # 富文本上传图片
    path('', views.home,name='home'),
    path('blog/',include('blog.urls')),                     # blog
    path('comment/',include('comment.urls')),               # 评论
    path('likes/',include('likes.urls')),                   # 点赞
    path('user/',include('user.urls')),                     # 用户相关

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
