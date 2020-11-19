# Generated by Django 2.2.10 on 2020-11-18 16:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Порядковый номер')),
                ('text', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Текст варианта')),
            ],
            options={
                'verbose_name': 'Вариант ответа',
                'verbose_name_plural': 'Варианты ответов',
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('starts', models.DateField(blank=True, null=True, verbose_name='Дата старта опроса')),
                ('ends', models.DateField(blank=True, null=True, verbose_name='Дата окончания опроса')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Опрос',
                'verbose_name_plural': 'Опросы',
                'ordering': ('-starts',),
            },
        ),
        migrations.CreateModel(
            name='Respondent',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Имя')),
                ('polls', models.ManyToManyField(to='polls.Poll', verbose_name='Выбранные опросы')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(blank=True, default=1, null=True, verbose_name='Порядковый номер')),
                ('text', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Текст вопроса')),
                ('answer_type', models.SmallIntegerField(blank=True, choices=[(1, 'ответ текстом'), (2, 'ответ с выбором одного варианта'), (3, 'ответ с выбором нескольких вариантов')], null=True, verbose_name='Тип ответа')),
                ('options', models.ManyToManyField(to='polls.Option', verbose_name='Варианты ответа')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll_questions', to='polls.Poll', verbose_name='Опрос')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ('number',),
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(blank=True, max_length=255, null=True, verbose_name='Текст ответа')),
                ('options', models.ManyToManyField(to='polls.Option', verbose_name='Выбранные варианты')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question', verbose_name='Ответ')),
                ('respondent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='respondent_answers', to='polls.Respondent', verbose_name='Опрос')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]