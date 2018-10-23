from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import redirect, render
from django.views.generic import View

from app.forms import UserForm


class LoginView(View):
    template_name = 'app/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            return redirect('/login')


class JoinView(View):
    template_name = 'app/join.html'

    def get(self, request):
        return render(request, self.template_name, {
            'form': UserForm(initial={
                'username': '',
                'email': '',
            })
        })

    def post(self, request):
        form = UserForm(request.POST, initial={
            'username': '',
            'email': '',
        })
        if form.is_valid():
            new_user = get_user_model().objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('/')
        else:
            return render(request, self.template_name, {
                form: form
            })


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')
