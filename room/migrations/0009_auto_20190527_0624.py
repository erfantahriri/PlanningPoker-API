# Generated by Django 2.2.1 on 2019-05-27 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_issue_vote_cards_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issues', to='room.Room', verbose_name='Room'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='room.Room', verbose_name='Room'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='room.Participant', verbose_name='Participant'),
        ),
    ]
