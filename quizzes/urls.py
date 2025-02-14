from django.urls import path, re_path

from .views import home, category, quiz
from .consumers import QuizConsumer

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', category, name='category'),
    path('quiz/<int:quiz_id>/', quiz, name='quiz'),
]

ws_urlpatterns = [
    re_path(r'ws/quiz/(?P<quiz_id>\d+)/$', QuizConsumer.as_asgi()),
]