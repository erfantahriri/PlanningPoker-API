from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0012_room_card_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='role',
            field=models.CharField(
                choices=[
                    ('dev', 'Developer'),
                    ('designer', 'Designer'),
                    ('pm', 'Product Manager'),
                    ('em', 'Eng Manager'),
                    ('voter', 'Voter'),
                    ('spectator', 'Spectator'),
                ],
                default='voter',
                max_length=16,
                verbose_name='Role',
            ),
        ),
    ]
