from rest_framework import viewsets, mixins, permissions
from rest_framework.generics import get_object_or_404
from .serializers import *
from datetime import datetime
from django.utils.timezone import make_aware

class PollViewSet(viewsets.ModelViewSet):
    '''
    Все опросы(сортировка по дате старта опроса от новых к более старым) не зависимо от пользователя.
    Создание опроса(только Админ(ы)).
    '''
    queryset = Poll.objects.all().order_by('-date_start')
    serializer_class = PollSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class ActivePollListViewSet(viewsets.ModelViewSet):
    '''
    Все активные на текущий момент опросы.
    Принцип: Дата начала опроса <= текущая дата <= дата конца опроса.
    Создание опроса(только Админ(ы)).
    '''
    queryset = Poll.objects.filter(
            date_start__lte=make_aware(datetime.today()),
            date_end__gte=make_aware(datetime.today()),
        ).order_by('-date_start')
    serializer_class = PollSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class QuestionViewSet(viewsets.ModelViewSet):
    '''
    Все вопросы(без фильтрации).
    Добавить вопросы(только Админ(ы)). 
    '''
    queryset = Question.objects.all().order_by('-id')
    serializer_class = QuestionSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class AnswerOptionViewSet(viewsets.ModelViewSet):
    '''
    Варианты ответов(без фильтрации).
    Добавить варианты ответов для вопросов(только Админ(ы)). 
    '''
    queryset = AnswerOption.objects.all().order_by('-id')
    serializer_class = AnswerOptionSerializer
    permission_classes = (permissions.IsAdminUser,)
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

class AnswerViewSet(viewsets.ModelViewSet):
    '''
    Ответы(без фильтрации).
    '''
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAdminUser,)
    
class AnswerCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    Прохождение опроса
    '''
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            poll__id=self.kwargs['id'],
        )
        if question.type == 'TEXT':
            return AnswerOneTextSerializer
        elif question.type == 'ONE':
            return AnswerOneChoiceSerializer
        else:
            return AnswerMultipleChoiceSerializer

    def perform_create(self, serializer):
        question = get_object_or_404(
            Question,
            pk=self.kwargs['question_pk'],
            poll__id=self.kwargs['id'],
        )
        serializer.save(user=self.request.user, question=question)

class CompletedPollsViewSet(viewsets.ModelViewSet):
    '''
    Пройденные опросы(текущий пользователь)
    '''
    serializer_class = CompletedPollsSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Poll.objects.exclude(~Q(question__answers__user__id=user_id))
        return queryset
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'POST']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

