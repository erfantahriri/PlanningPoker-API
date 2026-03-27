from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0010_participant_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Is Private'),
        ),
        migrations.AddField(
            model_name='room',
            name='password',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='Password'),
        ),
    ]
