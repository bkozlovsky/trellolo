from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Card, STATUSES

class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}), max_length=32, help_text='First name')
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}), max_length=32, help_text='Last name')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), max_length=64, help_text='Enter a valid email address')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat Password'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Username',
        }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Password',
        }
    ))

class CardCreateForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a title for this card...'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a more detailed description...'}))
    assignee = forms.ModelChoiceField(empty_label="", required=False, queryset=User.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Card
        fields = ('name', 'description', 'assignee')

    def __init__(self, *args, **kwargs):

        if 'request' in kwargs:

            self.request = kwargs.pop("request")
            super(CardCreateForm, self).__init__(*args, **kwargs)

            if self.request.user.is_superuser == False:

                self.fields['assignee'].queryset = User.objects.filter(username=self.request.user)


        elif 'queryset' in kwargs:

            queryset = kwargs.pop('queryset')
            super(CardCreateForm, self).__init__(*args, **kwargs)
            self.fields['assignee'].queryset = queryset

        else:

            super(CardCreateForm, self).__init__(*args, **kwargs)


class CardUpdateForm(CardCreateForm):

    status = forms.ChoiceField(choices=STATUSES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Card
        fields = ('name', 'description', 'assignee', 'status')
