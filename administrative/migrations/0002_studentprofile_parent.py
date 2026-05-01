import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrative', '0001_initial'),
        ('accounts', '0002_institution_admin_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                limit_choices_to={'role': 'padre'},
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='children_profiles',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
