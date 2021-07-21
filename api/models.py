from django.db import models
from django.conf import settings

class Poll(models.Model):
    '''Опросы'''
    title = models.CharField(verbose_name='Наименование опроса', max_length=256)
    date_start = models.DateTimeField(verbose_name='Дата старта опроса')
    date_end = models.DateTimeField(verbose_name='Дата окончания опроса', blank=True, null=True)
    description = models.CharField(verbose_name='Описание опроса', max_length=1000, blank=True, null=True)

    def __str__(self):
         return '%s' % (self.title)

class Question(models.Model):
    '''Вопросы для опросов'''
    ONE = 'ONE'
    TYPE_QUESTION = [
        ('TEXT', 'Ответ текстом'),
        ('ONE', 'Ответ с выбором одного варианта'),
        ('MULTIPLE', 'Ответ с выбором нескольких вариантов'),
        ]
    poll = models.ForeignKey(Poll, related_name='question', blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст вопроса', max_length=2000)
    type = models.CharField(verbose_name='Тип вопроса', max_length=8, choices=TYPE_QUESTION, default=ONE)

    def __str__(self):
        return '%s' % (self.text)


class AnswerOption(models.Model):
    '''Варианты ответов вопросов'''
    question = models.ForeignKey(Question, related_name='answer_option', blank=True, null=True, on_delete=models.CASCADE)
    text = models.CharField(verbose_name='Текст варианта ответа', max_length=500)

    def __str__(self):
        return '%s' % (self.text)


class Answer(models.Model):
    '''Ответы на вопросы'''
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    question = models.ForeignKey(Question, related_name='answers', blank=True, null=True, on_delete=models.CASCADE)
    multiple_answer = models.ManyToManyField(AnswerOption, blank=True)
    one_answer = models.ForeignKey(AnswerOption, related_name='one_answer', blank=True, null=True, on_delete=models.CASCADE)
    text_answer = models.TextField(verbose_name='Текст ответа', max_length=1000, blank=True, null=True)
