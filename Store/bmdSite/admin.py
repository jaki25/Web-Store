from django.contrib import admin
from .models import Store, Article, Type_Article
# Register your models here.

class AdminStore(admin.ModelAdmin):
    list_display=("name", "address")
    prepopulated_fields = {"slug":("name",)}

admin.site.register(Store, AdminStore)
admin.site.register(Article)
admin.site.register(Type_Article)