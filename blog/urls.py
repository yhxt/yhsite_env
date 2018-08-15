from django.urls import path
from . import views

urlpatterns = [
    path('',views.blog_list,name='blog_list'),
    path('<int:blog_pk>',views.blog_detail,name='blog_detail'),
    path('blog_type/<int:blog_type_pk>',views.blogs_with_type,name='blogs_with_type'),
    path('blog_author/<int:blog_author_pk>',views.blogs_with_author,name='blogs_with_author'),
    path('date/<int:year>/<int:month>',views.blogs_with_date,name='blogs_with_date'),
]
