from django.db import models


class Quiz(models.Model):
    name = models.CharField(max_length=40)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    times_taken = models.IntegerField(default=0)
    high_score = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    ansewer_text = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    answered_times = models.IntegerField(default=0)
    correct_answered_times = models.IntegerField(default=0)

    def __str__(self):
        return self.question_text