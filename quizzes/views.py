from django.shortcuts import render

from .models import Category, Question

# Create your views here.
def index(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def quiz(request, quiz_id: int):
    quiz_questions = Question.objects.filter(quiz=quiz_id)
    return render(request, 'quiz.html', context={'questions': quiz_questions})