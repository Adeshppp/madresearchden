# Generated by Django 2.0.5 on 2018-08-18 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeoKeywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='blogpost',
            name='seo_description',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seokeywords',
            name='blogpost',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogPost'),
        ),
    ]
