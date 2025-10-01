from django.db import models

class Article(models.Model):

    topic = models.CharField(max_length=100, default='Python')
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    main_image = models.ImageField(upload_to='articles_images/', null=True, blank=True)
    ap_time = models.IntegerField(default=1)

    def __str__(self):
        return self.title