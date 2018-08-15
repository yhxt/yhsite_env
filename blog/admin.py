from django.contrib import admin

from .models import Blog_type,Blog


class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')
    ordering = ('-id',)


class BlogAdmin(admin.ModelAdmin):
    list_display =('id','title','author','get_read_num','is_delete','created_time','last_update_time')
    ordering=('-id',)


admin.site.register(Blog_type,BlogtypeAdmin)
admin.site.register(Blog,BlogAdmin)
