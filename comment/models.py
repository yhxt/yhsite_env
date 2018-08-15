import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        '''初始化传入发送邮件所需参数'''
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        # 本身初始化函数也执行一下
        threading.Thread.__init__(self)

    def run(self):
        '''执行多线程会自动执行run()方法'''
        send_mail(
            self.subject, 
            '',
            # self.text, 
            settings.EMAIL_HOST_USER, 
            [self.email], 
            fail_silently=self.fail_silently,
            html_message=self.text
        )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    user = models.ForeignKey(User,related_name='comments',on_delete=models.CASCADE,verbose_name='评论者')

    root = models.ForeignKey('self',null=True,related_name='root_comment',on_delete=models.CASCADE)
    parent = models.ForeignKey('self',null=True,related_name='parent_comment',on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User,related_name='replies',null='True',on_delete=models.CASCADE)

    def send_email(self):
        '''评论邮件通知'''
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            # text = self.text + '\n' + self.content_object.get_url()
            # text = '%s\n<a href="%s">%s</a>' % (self.text, self.content_object.get_url(),'点击查看')
            context = {}
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context)
            # 使用多线程发送邮件
            send_mail = SendMail(subject, text, email)
            send_mail.start()   # 开启多线程

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-comment_time']
        verbose_name = '评论'
        verbose_name_plural = verbose_name



