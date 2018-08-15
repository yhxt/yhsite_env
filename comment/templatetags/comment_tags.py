from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


# 评论数
@register.simple_tag
def get_comment_count(obj):
    # 获取模型的类型
    content_type = ContentType.objects.get_for_model(obj)
    # 返回obj模型下obj.pk文章的评论总数
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


# 评论框
@register.simple_tag
def get_comment_form(obj):
    # 获取模型的类型
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
        'content_type':content_type.model,
        'object_id':obj.pk,
        'reply_comment_id': 0})
    return form


# 评论内容列表显示
@register.simple_tag
def get_comment_list(obj):
    # 获取模型的类型
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(
        content_type=content_type, 
        object_id=obj.pk, parent=None).order_by('-comment_time')
    return comments