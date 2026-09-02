from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    level = models.CharField(
        max_length=20,
        choices=[
            ('beginner', 'Начинающий'),
            ('intermediate', 'Средний'),
            ('advanced', 'Продвинутый'),
        ],
        default='beginner'
    )
    last_course_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

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

    short_description = models.CharField(max_length=300, default="This is the description of this course")

    image = models.URLField(blank=True, null=True, help_text="Ссылка на обложку курса")

    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta(CourseAndTimeStamp.Meta):
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Module(CourseAndTimeStamp):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="modules")

    def __str__(self):
        return f"{self.course.title} - {self.title}"
    
    class Meta(CourseAndTimeStamp.Meta):
        constraints = [
        models.UniqueConstraint(
            fields=["course", "order"],
            name="unique_module_order_in_course",
        )
    ]


class Topic(CourseAndTimeStamp):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="topics")

    def __str__(self):
        return f"{self.title} | {self.order}"

    class Meta(CourseAndTimeStamp.Meta):
        constraints = [
        models.UniqueConstraint(
            fields=["module", "order"],
            name="unique_topic_order_in_module",
        )
    ]


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

class UserCourseProgress(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="course_progress")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)


    class Meta:
        unique_together = ('course', 'user')


class UserTopicProgress(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="topic_progress",
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name="user_progress",
        )
    completed = models.BooleanField(default=False)


class Achievment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="achievments")
    title = models.CharField(max_length=255)
    small_description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    icon = models.ImageField(upload_to="achievment_icons/", null=True, blank=True)

    

        



