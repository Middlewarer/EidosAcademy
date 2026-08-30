from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Topic)
admin.site.register(TopicLesson)
admin.site.register(UserCourseProgress)
admin.site.register(UserTopicProgress)
admin.site.register(Achievment)