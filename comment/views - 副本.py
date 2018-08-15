


def update_comment(request):
    text = request.POST.get('text','')
    content_type = request.POST.get('content_type','')
    object_id = int(request.POST.get('object_id',''))
    model_class = ContentType.objects.get(model=content_type).model_class()
    model_object = model_class.objects.get(pk=object_id)

    comment = Comment()
    comment.user = request.user
    comment.text = text
    comment.content_object = model_object
    comment.save()
    referer = request.META.get('HTTP_REFERER',reverse('home'))
    return redirect(referer)