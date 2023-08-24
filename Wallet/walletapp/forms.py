# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Account, Transaction

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class AddAccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = '__all__'  # Include all fields from the Account model
        labels = {
            'name': 'Account Name'  # Customize the label for the 'name' field
        }

class AddTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'transaction_type','category', 'subcategory', 'date', 'amount', 'budget', 'description']

    date = forms.DateTimeField(widget=forms.TextInput(attrs={'type': 'date'}))