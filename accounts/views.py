from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login

from .forms import QuizzerUserCreationForm

class SignUpView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = QuizzerUserCreationForm
    success_url = reverse_lazy('quizzes:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response
