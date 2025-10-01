from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Course)
admin.site.register(models.TopicsBlock)
admin.site.register(models.Topic)
admin.site.register(models.Category)
admin.site.register(models.Content)
admin.site.register(models.UserTopicProgress)