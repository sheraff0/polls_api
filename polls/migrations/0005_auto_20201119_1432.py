# Generated by Django 2.2.10 on 2020-11-19 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20201119_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='polls.Question', verbose_name='Вопрос'),
        ),
    ]
