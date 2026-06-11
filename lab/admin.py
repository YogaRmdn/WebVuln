from django.contrib import admin
from .models import BlogPost, Comment, Product, UploadedFile

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Product)
admin.site.register(UploadedFile)
