# Generated manually to fix notification sender field
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_notification_result'),
    ]

    operations = [
        # Add sender field to Notification
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(
                blank=True, 
                null=True, 
                on_delete=django.db.models.deletion.SET_NULL, 
                related_name='triggered_notifications', 
                to=settings.AUTH_USER_MODEL, 
                verbose_name='المرسل'
            ),
        ),
    ]
