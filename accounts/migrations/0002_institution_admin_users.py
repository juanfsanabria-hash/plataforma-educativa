from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution',
            name='admin_users',
            field=models.ManyToManyField(
                blank=True,
                limit_choices_to={'role__in': ['admin', 'director']},
                related_name='admin_institutions',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
