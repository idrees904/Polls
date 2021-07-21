from .models import *
from rest_framework import serializers
from django.db.models import Q

class PollSerializer(serializers.ModelSerializer):
    '''Все опросы'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('date_start').read_only = True
   
    class Meta:
        model = Poll
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    '''Все вопросы'''
    class Meta:
        model = Question
        fields = '__all__'

class AnswerOptionSerializer(serializers.ModelSerializer):
    '''Варианты ответов'''
    class Meta:
        model = AnswerOption
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    '''Ответы'''
    class Meta:
        fields = '__all__'
        model = Answer

class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    '''Фильтрация по пользователю'''
    def get_queryset(self):
        question_id = self.context.get('request').parser_context['kwargs']['question_pk']
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(question_id=question_id)

class AnswerOneTextSerializer(serializers.ModelSerializer):
    '''Ответы текстом'''
    class Meta:
        fields = ['text_answer']
        model = Answer

class AnswerOneChoiceSerializer(serializers.ModelSerializer):
    '''Ответы выбором одного варианта'''
    one_answer = UserFilteredPrimaryKeyRelatedField(
        many=False,
        queryset=AnswerOption.objects.all()
    )

    class Meta:
        fields = ['one_answer']
        model = Answer

class AnswerMultipleChoiceSerializer(serializers.ModelSerializer):
    '''Ответ выбором множества вариантов'''
    multiple_answer = UserFilteredPrimaryKeyRelatedField(
        many=True,
        queryset=AnswerOption.objects.all()
    )

    class Meta:
        fields = ['multiple_answer']
        model = Answer

class AnswersAndAnswerOptionSerializer(serializers.ModelSerializer):
    '''Детализация по вариантам ответов'''
    multiple_answer = AnswerOptionSerializer(many=True,read_only=True)    
    one_answer = AnswerOptionSerializer(many=False, read_only=True)
    
    class Meta:
        model = Answer
        fields = ('id','user', 'question', 'text_answer', 'one_answer', 'multiple_answer')

class QuestionsAndAnswersSerializer(serializers.ModelSerializer):
    '''Детализация по вопросам и ответам'''
    answers = serializers.SerializerMethodField('get_answers')

    class Meta:
        model = Question
        fields = ('id','poll', 'text', 'type', 'answers')

    def get_answers(self, question):
        user_id = self.context.get('request').user.id
        answers = Answer.objects.filter(Q(question=question) & Q(user__id=user_id))
        serializer = AnswersAndAnswerOptionSerializer(instance=answers, many=True, read_only=True)
        return serializer.data

class CompletedPollsSerializer(serializers.ModelSerializer):
    '''Пройденные опросы с детализацией по вопросам и ответам'''
    question = QuestionsAndAnswersSerializer(many=True, read_only=True)
    
    class Meta:
        model = Poll
        fields = ('id','title', 'date_start', 'date_end', 'description', 'question')