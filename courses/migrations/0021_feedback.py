from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("courses", "0020_course_progress_last_topic"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(choices=[("review", "Отзыв"), ("idea", "Пожелание"), ("bug", "Ошибка")], max_length=10)),
                ("name", models.CharField(blank=True, max_length=80)),
                ("contact", models.EmailField(blank=True, max_length=254)),
                ("message", models.TextField(max_length=2000)),
                ("page_url", models.URLField(blank=True, max_length=500)),
                ("status", models.CharField(choices=[("new", "Новое"), ("seen", "Просмотрено"), ("planned", "Запланировано"), ("resolved", "Исправлено"), ("rejected", "Отклонено")], default="new", max_length=10)),
                ("is_public", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="feedback_entries", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
