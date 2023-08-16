from django.contrib import admin
from blog.models import Post , Comment
# Register your models here.

@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    list_display = ['pk','author','title','data_create']
    list_display_links = ['author','title']
    prepopulated_fields = {"slug": ("title",) }

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','name_author','data_create']
    list_display_links = ['name_author','post']