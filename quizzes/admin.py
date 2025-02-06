from django.contrib import admin

from .models import Question, Quiz, Category

admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Category)