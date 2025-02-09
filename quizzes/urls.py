from django.urls import path
from .views import home, category, quiz

urlpatterns = [
    path('', home, name='home'),
    path('category/<int:category_id>/', category, name='category'),
    path('quiz/<int:quiz_id>/', quiz, name='quiz'),
]