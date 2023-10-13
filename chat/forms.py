from django import forms
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import ChatRoom


from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'User Name'})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class RegistrationForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2','first_name', 'last_name', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2
    
class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ChatRoom.objects.filter(name=name).exists():
            raise forms.ValidationError("A chat room with this name already exists.")
        return name
    

class MessageForm(forms.Form):
    content = forms.CharField(widget=forms.TextInput(attrs={'class': 'message-input'}))
