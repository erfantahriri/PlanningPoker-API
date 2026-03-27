from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0009_auto_20190527_0624'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='role',
            field=models.CharField(
                choices=[('voter', 'Voter'), ('spectator', 'Spectator')],
                default='voter',
                max_length=16,
                verbose_name='Role',
            ),
        ),
    ]
