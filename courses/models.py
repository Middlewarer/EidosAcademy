from django.db import models

class CourseAndTimeStamp(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="Порядок сортировки")

    class Meta:
        abstract = True
        ordering = ['order']

class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Course(CourseAndTimeStamp):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT, 
        related_name='courses'
    )

    image = models.URLField(blank=True, null=True, help_text="Ссылка на обложку курса")

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta(CourseAndTimeStamp.Meta):
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Module(CourseAndTimeStamp):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    class Meta(CourseAndTimeStamp.Meta):
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'


class Topic(CourseAndTimeStamp):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} | {self.order}"

    class Meta(CourseAndTimeStamp.Meta):
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'


class TopicLesson(models.Model):
    TYPE_CHOICES = (
        ('video', 'Video'),
        ('text', 'Text'),
        ('equal', 'Equal_task'),
    )

    type = models.CharField(max_length=6, choices=TYPE_CHOICES, default='text')
    content = models.TextField(blank=True)
    video_url = models.URLField(blank=True, null=True, )
    parent_topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.PositiveSmallIntegerField(default=0, help_text="Порядок сортировки")

    class Meta(CourseAndTimeStamp.Meta):
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f'{self.parent_topic.title} | {self.order}'
        



