from django.db.models import Prefetch
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.decorators import action, permission_classes
from .models import (
    Poll, Option, Question,
    Respondent, Answer
)
from .serializers import (
    PollSerializer, PollNestedSerializer, PollNestedQASerializer,
    OptionSerializer,
    QuestionSerializer, QuestionNestedSerializer,
    RespondentSerializer, RespondentNestedSerializer,
    AnswerSerializer
)


@permission_classes([IsAdminUser])
class BaseViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]


class WithNested:

    def list(self, request):
        queryset = super().get_queryset().prefetch_related(
            *self.prefetch_list)
        serializer = self.detail_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = super().get_queryset().prefetch_related(
            *self.prefetch_list)
        obj = queryset.filter(pk=pk).first()
        serializer = self.detail_serializer(obj)
        return Response(serializer.data)


class PollViewSet(WithNested, BaseViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    prefetch_list = [Prefetch(
        'poll_questions',
        Question.objects.prefetch_related('options')
    )]
    detail_serializer = PollNestedSerializer

    def update(self, request, pk=None, **kwargs):
        obj = self.get_object()
        request.data['starts'] = obj.starts or request.data['starts']
        return super().update(request, pk, **kwargs)

    def list(self, request):
        return super(BaseViewSet, self).list(request)

    @action(methods=['get'], detail=False, permission_classes=[AllowAny],
            url_path='active-list', url_name='active_list')
    def active_list(self, request):
        queryset = Poll.objects.active()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[AllowAny],
            url_path='get-poll', url_name='get_poll')
    def get_poll(self, request, pk=None):
        return self.retrieve(request, pk)


class OptionViewSet(BaseViewSet):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class QuestionViewSet(WithNested, BaseViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    http_method_names = ('get', 'post', 'put', 'delete')
    prefetch_list = ('options',)
    detail_serializer = QuestionNestedSerializer


class RespondentViewSet(WithNested, BaseViewSet):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer
    prefetch_list = ('polls',)
    detail_serializer = RespondentNestedSerializer

    @action(methods=['post'], detail=False, permission_classes=[AllowAny],
            url_path='add-respondent', url_name='add_respondent')
    def add_respondent(self, request):
        try:
            name = request.data.get('name')
        except Exception as e:
            return Response({"detail": e.__str__()})
        obj = Respondent.objects.create(name=name)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    @action(methods=['post'], detail=True, permission_classes=[AllowAny],
            url_path='add-poll', url_name='add_poll')
    def add_poll(self, request, pk=None):
        try:
            poll_id = request.data.get('poll_id')
            poll = Poll.objects.active().get(pk=poll_id)
        except Exception as e:
            return Response({"detail": e.__str__()})
        obj = self.get_object()
        obj.polls.add(poll)
        serializer = self.serializer_class(obj)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, permission_classes=[AllowAny],
            url_path='get-polls', url_name='get_polls')
    def get_polls(self, request, pk=None):
        queryset = self.get_object().polls.all().prefetch_related(Prefetch(
            'poll_questions',
            Question.objects.prefetch_related(Prefetch(
                'question_answers',
                Answer.objects.filter(respondent_id=pk)
            ), 'options')
        ))
        serializer = PollNestedQASerializer(queryset, many=True)
        return Response(serializer.data)


class AnswerViewSet(BaseViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    @action(methods=['post'], detail=False, permission_classes=[AllowAny],
            url_path='add-answer', url_name='add_answer')
    def add_answer(self, request, pk=None):
        try:
            question_id = request.data.get('question_id')
            question = Question.objects.get(pk=question_id)
            respondent_id = request.data.get('respondent_id')
            respondent = Respondent.objects.get(pk=respondent_id)
            respondent.polls.add(question.poll)
            obj, _ = Answer.objects.get_or_create(
                question=question,
                respondent=respondent
            )
            text = request.data.get('text')
            options = request.data.get('options')
            if question.answer_type == 1:
                obj.text = text
            elif question.answer_type == 2:
                obj.options.set(options[:1])
            elif question.answer_type == 3:
                obj.options.set(options)
            obj.save()
            serializer = AnswerSerializer(obj)
            return Response(serializer.data)
        except Exception as e:
            return Response({"detail": e.__str__()})
