from rest_framework import serializers
from .models import (
    Poll, Option, Question,
    Respondent, Answer
)
from polls_api.utils import fields_list


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionNestedSerializer(QuestionSerializer):
    options = OptionSerializer(many=True, read_only=True)


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = '__all__'


class PollNestedSerializer(PollSerializer):
    poll_questions = QuestionNestedSerializer(many=True, read_only=True)

    class Meta(PollSerializer.Meta):
        fields = [
            *fields_list(Poll),
            'poll_questions'
        ]


class RespondentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Respondent
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class AnswerNestedSerializer(AnswerSerializer):
    question = QuestionSerializer(read_only=True)


class QASerializer(QuestionNestedSerializer):
    question_answers = AnswerSerializer(many=True, read_only=True)


class PollNestedQASerializer(PollSerializer):
    poll_questions = QASerializer(many=True, read_only=True)


class RespondentNestedSerializer(RespondentSerializer):
    polls = PollNestedQASerializer(many=True, read_only=True)
