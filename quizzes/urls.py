from django.urls import path
from .views import index, quiz

urlpatterns = [
    path('', index, name='index'),
    path('quiz/<int:quiz_id>/', quiz, name='quiz'),
]