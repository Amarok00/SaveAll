from django.contrib import admin
from discussions.models import Discussions 
# Register your models here.

@admin.register(Discussions)
class PageAdmin(admin.ModelAdmin):
    list_display = ['pk','author','title','data_create']
    list_display_links = ['author','title']