# Generated by Django 2.2.10 on 2020-11-19 04:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20201118_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='options',
            field=models.ManyToManyField(to='polls.Option', verbose_name='Выбранные варианты'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='respondent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respondent_answers', to='polls.Respondent', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='respondent',
            name='polls',
            field=models.ManyToManyField(to='polls.Poll', verbose_name='Выбранные опросы'),
        ),
    ]
