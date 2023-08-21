from django import forms
from .models import Transaction, Category, Subcategory
from django.forms.widgets import PasswordInput, TextInput, EmailInput, FileInput, NumberInput, DateInput
from .models import CustomUser


from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Password', 'required':'required'}))
    password2 = forms.CharField(widget=PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password', 'required':'required'}))

    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','email','date_of_birth') 
        widgets = {
        'first_name':TextInput(attrs={'class':'form-control', 'placeholder':'First Name', 'required':'required'}),
        'last_name':TextInput(attrs={'class':'form-control', 'placeholder':'Last Name', 'required':'required'}),
        'email': EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'required':'required'}),
        'date_of_birth': DateInput(attrs={'class':'form-control', 'placeholder':'Date of Birth', 'required':'required','type': 'date'}),
    }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class CustomAuthForm(forms.Form): 
#     email = forms.CharField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'required':'required'}))
#     password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'required':'required'}))

class CustomAuthForm(forms.Form): 
    email = forms.CharField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'Email', 'required':'required'}))
    username = forms.CharField(widget=EmailInput(attrs={'class':'form-control', 'placeholder':'Username', 'required':'required'}))
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control','placeholder':'Password', 'required':'required'}))


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = '__all__'