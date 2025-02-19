from django.shortcuts import render, get_object_or_404

from .models import Category, Quiz, Question

# Create your views here.
def home(request):
    categories = Category.objects.filter(featured=True)
    quizzes = Quiz.objects.filter(featured=True)
    return render(request, 'home.html', {'categories': categories, 'quizzes': quizzes})

def category(request, category_id: int):
    quizzes = Quiz.objects.filter(category=category_id)
    featured_quizzes = Quiz.objects.filter(category=category_id, category_featured=True)
    category = Category.objects.get(id=category_id)
    return render(request, 'category.html', {'category': category, 'quizzes': quizzes, 'featured_quizzes': featured_quizzes})

def quiz(request, quiz_id: int):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz.html', {'quiz': quiz})