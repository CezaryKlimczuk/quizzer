from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField(null=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    name = models.CharField(max_length=40)
    featured = models.BooleanField(default=False)
    category_featured = models.BooleanField(default=False)
    category = models.ForeignKey(Category, related_name='quizzes', on_delete=models.CASCADE)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    times_taken = models.IntegerField(default=0)
    high_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    correct_answer_text = models.CharField(max_length=50)
    answer_options = models.JSONField(null=True, default=list)
    date_created = models.DateTimeField(auto_now_add=True)
    answered_times = models.IntegerField(default=0)
    correct_answered_times = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text