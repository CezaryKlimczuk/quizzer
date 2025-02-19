from django.urls import path

from .views import home, category, quiz
from .consumers import QuizConsumer, GlobalNotificationConsumer

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', category, name='category'),
    path('quiz/<int:quiz_id>/', quiz, name='quiz'),
]

ws_urlpatterns = [
    path('ws/quiz/<int:quiz_id>/', QuizConsumer.as_asgi()),
    path('ws/global_notifications/', GlobalNotificationConsumer.as_asgi())
]