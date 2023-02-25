# Generated by Django 4.1.7 on 2023-02-24 20:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_image_invent_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invent',
            name='desc',
        ),
        migrations.RemoveField(
            model_name='invent',
            name='exp_date',
        ),
        migrations.RemoveField(
            model_name='invent',
            name='image',
        ),
        migrations.RemoveField(
            model_name='invent',
            name='start_date',
        ),
        migrations.RemoveField(
            model_name='invent',
            name='status',
        ),
        migrations.AddField(
            model_name='invent',
            name='donor_id',
            field=models.ForeignKey(default='prakriti', on_delete=django.db.models.deletion.CASCADE, related_name='donor1', related_query_name='donor1', to='inventory.donor'),
        ),
    ]
