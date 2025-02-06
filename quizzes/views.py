from django.shortcuts import render

from .models import Quiz, Question

# Create your views here.
def index(request):
    quizes = Quiz.objects.all()
    return render(request, 'index.html', context={'quizzes': quizes})

def quiz(request, quiz_id: int):
    quiz_questions = Question.objects.filter(quiz=quiz_id)
    return render(request, 'quiz.html', context={'questions': quiz_questions})