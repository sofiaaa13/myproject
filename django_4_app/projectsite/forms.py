from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Post, Comment
from django import forms


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
        widgets = {'username': forms.TextInput(attrs={'class': 'log_f'}),
                   'email': forms.TextInput(attrs={'class': 'log_f'}),
                   'first_name': forms.TextInput(attrs={'class': 'log_f'}),
                   'last_name': forms.TextInput(attrs={'class': 'log_f'}),
                   'password1': forms.PasswordInput(attrs={'class': 'log_f'}),
                   'password2': forms.PasswordInput(attrs={'class': 'log_f'})}


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {'username': forms.TextInput(attrs={'class': 'log_f'}),
                   'password': forms.PasswordInput(attrs={'class': 'log_f'})}


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': "form_e", 'placeholder': 'Search'}))


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text': forms.TextInput(attrs={
                   'class': "form_e",
                   'placeholder': 'Add a comment...'})}


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['photo']
        widgets = {'photo': forms.FileInput(attrs={
                   'class': 'file_inpt'})}

