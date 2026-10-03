import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("courses", "0022_alter_course_image")]

    operations = [
        migrations.CreateModel(
            name="LegalAcceptance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("kind", models.CharField(choices=[("personal_data", "Согласие на обработку персональных данных"), ("terms", "Пользовательское соглашение"), ("publication", "Согласие на публикацию сообщения")], max_length=20)),
                ("document_version", models.CharField(max_length=20)),
                ("ip_address", models.GenericIPAddressField(blank=True, null=True)),
                ("user_agent", models.CharField(blank=True, max_length=500)),
                ("accepted_at", models.DateTimeField(auto_now_add=True)),
                ("feedback", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="legal_acceptances", to="courses.feedback")),
                ("user", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="legal_acceptances", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-accepted_at"]},
        ),
        migrations.AddIndex(
            model_name="legalacceptance",
            index=models.Index(fields=["kind", "accepted_at"], name="courses_leg_kind_aa02b3_idx"),
        ),
    ]
