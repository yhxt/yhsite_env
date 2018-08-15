from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation #7天内热门阅读点击
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod,ReadDetail

class Blog_type(models.Model):
    type_name=models.CharField(max_length=15,verbose_name=u'分类名')

    class Meta:
        verbose_name='分类'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.type_name

class Blog(models.Model,ReadNumExpandMethod):
    title=models.CharField(max_length=50,verbose_name=u'标题')
    blog_type=models.ForeignKey(Blog_type,on_delete=models.DO_NOTHING)
    content=RichTextUploadingField()
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,verbose_name='作者')
    read_details = GenericRelation(ReadDetail)  ##7天内热门阅读点击
    created_time=models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    last_update_time=models.DateTimeField(auto_now=True,verbose_name=u'修改时间')
    is_delete=models.BooleanField(default=False,verbose_name=u'是否删除')

    def get_url(self):
        # 返回博客对应链接
        return reverse('blog_detail',kwargs={'blog_pk': self.pk})

    def get_email(self):
        # 获取用户email
        return self.author.email
        
    class Meta:
        ordering=['-created_time']
        verbose_name='博客'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title

