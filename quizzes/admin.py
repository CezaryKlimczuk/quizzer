from django.contrib import admin

from .models import Question, Quiz, Category


@admin.action(description="Make quiz featured within category")
def add_to_category_featured(modeladmin, request, queryset):
    queryset.update(category_featured=True)

@admin.action(description="Remove quiz from featured within category")
def remove_from_category_featured(modeladmin, request, queryset):
    queryset.update(category_featured=False)

class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'times_taken', 'category_featured']
    list_filter = ['category']
    actions = [add_to_category_featured, remove_from_category_featured]

admin.site.register(Question)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Category)