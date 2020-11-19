import uuid
from django.db import models
from .managers import PollQueryset


class Poll(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название',
    )
    starts = models.DateField(
        null=True, blank=True,
        verbose_name='Дата старта опроса')
    ends = models.DateField(
        null=True, blank=True,
        verbose_name='Дата окончания опроса')
    description = models.CharField(
        max_length=255,
        verbose_name='Описание',
        null=True, blank=True,
    )
    objects = PollQueryset.as_manager()

    def __str__(self):
        return f'{self.name[:50]}...'

    class Meta:
        ordering = ('-starts',)
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Option(models.Model):
    number = models.PositiveSmallIntegerField(
        null=True, blank=True, default=1,
        verbose_name='Порядковый номер'
    )
    text = models.CharField(
        max_length=2048,
        verbose_name='Текст варианта',
        null=True, blank=True,
    )

    def __str__(self):
        return f'{self.number}-{self.text}'

    class Meta:
        ordering = ('number',)
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class Question(models.Model):
    ANSWER_TYPES = (
        (1, 'ответ текстом'),
        (2, 'ответ с выбором одного варианта'),
        (3, 'ответ с выбором нескольких вариантов'),
    )
    poll = models.ForeignKey(
        Poll,
        related_name="poll_questions",
        on_delete=models.CASCADE,
        verbose_name='Опрос',
    )
    number = models.PositiveSmallIntegerField(
        null=True, blank=True, default=1,
        verbose_name='Порядковый номер'
    )
    text = models.CharField(
        max_length=2048,
        verbose_name='Текст вопроса',
        null=True, blank=True,
    )
    answer_type = models.SmallIntegerField(
        choices=ANSWER_TYPES,
        verbose_name="Тип ответа",
        null=True, blank=True,
    )
    options = models.ManyToManyField(
        Option,
        verbose_name='Варианты ответа',
    )

    class Meta:
        ordering = ('number',)
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Respondent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=64,
        verbose_name='Имя',
    )
    polls = models.ManyToManyField(
        Poll,
        verbose_name='Выбранные опросы',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name="question_answers",
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
    )
    respondent = models.ForeignKey(
        Respondent,
        related_name="respondent_answers",
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
    )
    text = models.CharField(
        max_length=255,
        verbose_name='Текст ответа',
        null=True, blank=True,
    )
    options = models.ManyToManyField(
        Option,
        verbose_name='Выбранные варианты',
    )

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'
