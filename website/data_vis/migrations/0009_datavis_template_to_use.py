# Generated by Django 2.2.3 on 2019-07-27 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_vis', '0008_auto_20190719_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='datavis',
            name='template_to_use',
            field=models.CharField(choices=[['altair', 'altair'], ['bokeh', 'bokeh']], default='bokeh', max_length=10),
        ),
    ]
