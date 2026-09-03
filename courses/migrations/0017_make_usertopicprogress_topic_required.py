import django.db.models.deletion
from django.db import migrations, models


def remove_progress_without_topic(apps, schema_editor):
    UserTopicProgress = apps.get_model("courses", "UserTopicProgress")
    UserTopicProgress.objects.filter(topic__isnull=True).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0016_remove_usermoduleprogress_module_and_more"),
    ]

    operations = [
        migrations.RunPython(
            remove_progress_without_topic,
            migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="usertopicprogress",
            name="topic",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user_progress",
                to="courses.topic",
            ),
        ),
    ]
