from django.db import models
from django.contrib.auth.models import AbstractUser

from quizzes.models import Quiz

class QuizzerUser(AbstractUser):
    quizzes_completed = models.ManyToManyField(
        Quiz,
        blank=True,
        related_name="users_completed",
        help_text="Quizzes that this user has completed."
    )

    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.username


# Create your models here.
