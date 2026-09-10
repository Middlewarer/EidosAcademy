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


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('kind', 'name', 'status', 'is_public', 'created_at')
    list_filter = ('kind', 'status', 'is_public')
    search_fields = ('name', 'contact', 'message')
    readonly_fields = ('user', 'created_at')
    list_editable = ('status', 'is_public')
