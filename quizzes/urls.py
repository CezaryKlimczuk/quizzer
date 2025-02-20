from django.urls import path

from .views import home, categories_all, category, quiz
from .consumers import QuizConsumer, GlobalNotificationConsumer

urlpatterns = [
    path('', home, name='home'),
    path('category/all/', categories_all, name='categories_all'),
    path('category/<int:category_id>/', category, name='category'),
    path('quiz/<int:quiz_id>/', quiz, name='quiz'),
]

ws_urlpatterns = [
    path('ws/quiz/<int:quiz_id>/', QuizConsumer.as_asgi()),
    path('ws/global_notifications/', GlobalNotificationConsumer.as_asgi())
]