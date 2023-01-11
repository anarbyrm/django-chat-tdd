from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from django.views import View, generic
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from chat_users.forms import RegisterForm, FriendRequestForm
from chat_users.models import FriendRequest


User = get_user_model

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


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect('home')
        else:
            return redirect('home')


@login_required()
def send_friend_request(request, user_id):
    receiver = get_object_or_404(get_user_model(), id=user_id)
    if request.user not in receiver.friends.all():
        if request.user != receiver:
            friend_request = FriendRequest(
                sender=request.user,
                receiver=receiver,
            )
            friend_request.save()
            messages.success(request, "Your friend request has been sent successfully!")
            return redirect('home')
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseBadRequest()


@login_required()
def answer_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    sender = friend_request.sender
    form = FriendRequestForm()
    if friend_request.receiver == request.user:
        if request.method == "POST":
            form = FriendRequestForm(request.POST, instance=friend_request)
            if form.is_valid():
                status = form.cleaned_data['status']
                if status == 'A':
                    request.user.friends.add(sender)
                    sender.friends.add(request.user)
                    friend_request.delete()
                    return redirect('home')
                elif status == 'D':
                    friend_request.delete()
                    return redirect('home')
    else:
        return HttpResponseForbidden()


class FriendsListView(generic.TemplateView):
    template_name = 'friends_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friends'] = self.request.user.friends.all()
        return context


class RequestsListView(generic.TemplateView):
    template_name = 'requests_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requests'] = FriendRequest.objects.filter(receiver=self.request.user)
        return context