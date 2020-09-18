from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import CrmUser

class SignUpForm (UserCreationForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs = {
            "id": "exampleInputName1",
            "name": "first_name"
        })
    )

    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs = {
            "id": "exampleInputName1",
            "name": "last_name"
        })
    )

    email = forms.CharField(
        max_length=100,
        widget=forms.EmailInput(attrs = {
            "id": "exampleInputEmail1",
            "name": "email"
        })
    )

    class Meta:
        model = CrmUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm (forms.Form):
     email = forms.CharField (
        max_length=100,
        widget=forms.EmailInput(attrs = {
            "id": "exampleInputEmail1"
        })
    )

     password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs = {
            "id": "exampleInputPassword1"
        })
    )
