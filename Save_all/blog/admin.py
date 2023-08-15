from django.contrib import admin
from blog.models import Post 
# Register your models here.

@admin.register(Post)
class PageAdmin(admin.ModelAdmin):
    list_display = ['pk','author','title','data_create']
    list_display_links = ['author','title']
    prepopulated_fields = {"slug": ("title",) }