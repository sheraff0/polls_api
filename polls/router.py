from rest_framework import routers
from .views import (
    PollViewSet, OptionViewSet, QuestionViewSet,
    RespondentViewSet, AnswerViewSet
)

router = routers.DefaultRouter()

router.register('polls', PollViewSet)
router.register('options', OptionViewSet)
router.register('questions', QuestionViewSet)
router.register('respondents', RespondentViewSet)
router.register('answers', AnswerViewSet)
