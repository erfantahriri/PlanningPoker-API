from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0011_room_private_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='card_set',
            field=models.CharField(
                choices=[('standard', 'Standard'), ('fibonacci', 'Fibonacci'), ('tshirt', 'T-Shirt Sizes')],
                default='standard', max_length=32, verbose_name='Card Set'
            ),
        ),
    ]
