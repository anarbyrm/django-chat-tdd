from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout

from chat_users.forms import RegisterForm


class RegisterView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = RegisterForm()
            context = dict(form=form)
            return render(request, 'register.html', context)
        else:
            return redirect(reverse('home'))

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('accounts:login'))
            else:
                context = dict(form=form, errors=form.errors)
                return render(request, 'register.html', context, status=400)
        else:
            return redirect(reverse('home'))


class UserLoginView(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse('home') 
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class UserLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')
        else:
            return redirect('home')
