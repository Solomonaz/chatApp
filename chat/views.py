from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import RegistrationForm
from . models import CustomUser, ChatRoom, Message
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required




class RegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            self.user = form.get_user()
            login(self.request, self.user)
            return redirect(self.get_success_url())

        context = self.get_context_data(form=form)
        context['login_error'] = "Invalid username"
        return render(self.request, self.template_name, context)

    def form_invalid(self, form):
        print("Invalid login attempt")
        return super().form_invalid(form)


class CustomLogoutView(LogoutView):
    next_page = 'login' 


def index(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    last_activity_user = CustomUser.objects.latest('last_activity')
    last_activity_time = last_activity_user.last_activity
    
    current_time = datetime.now(tz=timezone.utc)

    time_difference = current_time - last_activity_time
    if time_difference.total_seconds() < 60:
        user_status = f'{int(time_difference.total_seconds())} minutes ago'
    else:
        hours = int(time_difference.total_seconds() / 3600)
        user_status = f'Last seen {hours} hr ago'

    # if request.method == 'POST':
    #     content = request.POST.get('content')
    #     sender = request.user
    #     recipient = users[1:]

    #     message_content = Message(
    #        content = content,
    #        sender = sender,
    #        recipient = recipient,
    #     )
    #     message_content.save()
    #     return redirect('index')
    context = {
        'users': users,
        'user_status': user_status,
    }
    return render(request, "index.html", context)



def chatpage(request, username):
    user_obj = CustomUser.objects.get(username=username)
    users = CustomUser.objects.exclude(username=request.user.username)

    if request.method == 'POST':
        content = request.POST.get('content')
        sender = request.user
        recipient = CustomUser.objects.get(username=username)
        room = ChatRoom.objects.filter(sender=sender, participants=recipient).first()

        message = Message.objects.create(
            room=room,
            content=content,
            sender=sender,
            recipient=recipient
        )
        message.save()
        return redirect('chatpage', username=username)
    context = {
        'user_obj':user_obj, 
        'users':users,
    }
    return render(request, "chat/room.html", context)



# @login_required
# def submit_message(request, username):
#     if request.method == 'POST':
#         content = request.POST.get('content')
#         sender = request.user
#         recipient = CustomUser.objects.get(username=username)

#         message = Message.objects.create(
#             room=None,
#             content=content,
#             sender=sender,
#             recipient=recipient
#         )
#         message.save()

#         return redirect('chatpage', username=username)