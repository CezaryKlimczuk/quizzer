from django.shortcuts import render

from .models import Category, Quiz, Question

# Create your views here.
def home(request):
    categories = Category.objects.filter(featured=True)
    quizzes = Quiz.objects.filter(featured=True)
    return render(request, 'home.html', {'categories': categories, 'quizzes': quizzes})

def category(request, category_id: int):
    quizzes = Quiz.objects.filter(category=category_id)
    featured_quizzes = Quiz.objects.filter(category=category_id, featured=True)
    category = Category.objects.get(id=category_id)
    return render(request, 'category.html', {'category': category, 'quizzes': quizzes, 'featured_quizzes': featured_quizzes})

def quiz(request, quiz_id: int):
    quiz_questions = Question.objects.filter(quiz=quiz_id)
    return render(request, 'quiz.html', context={'questions': quiz_questions})