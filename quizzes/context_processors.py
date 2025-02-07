from quizzes.models import Category, Quiz

def categories_processor(request):
    return {
        'categories': Category.objects.all(),
    }
