from dataclasses import field
from django import forms
from .models import Product, CustomUser, UserCompany

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'repeat_password')

    def clean(self):
        data = self.cleaned_data
        if data.get('password') != data.get('repeat_password'):
            raise forms.ValidationError('Passwords do not match!')
        return data

class NewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class UserCompanyForm(forms.ModelForm):
    class Meta:
        model = UserCompany
        fields = '__all__'