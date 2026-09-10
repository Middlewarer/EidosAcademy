from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0019_usercourseprogress_assigned_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usercourseprogress",
            name="assigned_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AddField(
            model_name="usercourseprogress",
            name="last_topic",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="last_opened_by",
                to="courses.topic",
            ),
        ),
        migrations.AddField(
            model_name="usertopicprogress",
            name="last_visited_at",
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
