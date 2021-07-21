from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'all_polls', views.PollViewSet, basename='all-polls')
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)
router.register(r'answers_options', views.AnswerOptionViewSet)

router.register(r'active_polls', views.ActivePollListViewSet, basename='active-polls')
router.register(
    r'polls/(?P<id>\d+)/questions/(?P<question_pk>\d+)',
    views.AnswerCreateViewSet,
    basename='take-survey'
)
router.register(r'complete_polls', views.CompletedPollsViewSet, basename='complete-polls')


urlpatterns = [
    path('', include(router.urls)),
]