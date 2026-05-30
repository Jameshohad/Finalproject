# Generated for the final project premium demonstration.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="is_premium",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="is_premium",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="user",
            name="premium_until",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
