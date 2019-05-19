# Generated by Django 2.2.1 on 2019-05-18 20:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0006_participant_is_creator'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='current_issue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='room.Issue', verbose_name='Current Issue'),
        ),
        migrations.AlterField(
            model_name='vote',
            name='issue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='room.Issue', verbose_name='Issue'),
        ),
    ]