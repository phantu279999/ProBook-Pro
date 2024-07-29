from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.News)
admin.site.register(models.NewsContent)
admin.site.register(models.Category)
admin.site.register(models.CategoryNews)
admin.site.register(models.Tag)
admin.site.register(models.TagNews)
admin.site.register(models.Topic)
admin.site.register(models.TopicNews)
