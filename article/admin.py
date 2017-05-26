from django.contrib import admin

# Register your models here.

from article.models import Article, UploadFileForm

# Register your models here.


admin.site.register(Article)
admin.site.register(UploadFileForm)
