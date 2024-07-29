from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from .models import User, User_Profile
from courses.models import Courses, Tags

class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(label= "Phone Number:", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}), required=False)
    address1 = forms.CharField(label= "Address 1", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}), required=False)
    address2 = forms.CharField(label= "Address 2(optional)", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}), required=False)
    city = forms.CharField(label= "City", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}), required=False)
    state = forms.CharField(label= "State", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
    zipcode = forms.CharField(label= "Zipcode", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}), required=False)
    country = forms.CharField(label= "Country", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}), required=False)
    
    class Meta:
        model = User_Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country')


class ChangeUserPassword(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}), label='Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}), label='Confirm Password')
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

class UserUpdateForm(UserChangeForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    university = forms.ChoiceField(choices=User.UNIVERSITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))
    is_creator = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Is Creator')

    class Meta:
        model = User
        fields = ['username', 'age', 'email', 'university', 'is_creator']

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    university = forms.ChoiceField(choices=User.UNIVERSITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control form-control-lg'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}), label='Confirm Password')
    is_creator = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), label='Is Creator')

    class Meta:
        model = User
        fields = ['username', 'age', 'email', 'university', 'password1', 'password2', 'is_creator']

class User_Add_Course_Form(forms.ModelForm):
    new_tags = forms.CharField(
        max_length=200,
        required=False,
        help_text='Enter a tag for the course',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'})
    )
    
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'})
    )
    price = forms.DecimalField(
        decimal_places=2,
        max_digits=6,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'})
    )
    description = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg'})
    )
    context = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control form-control-lg'})
    )
    youtube_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control form-control-lg'}),
        help_text='Enter a YouTube URL if applicable.'
    )
    is_sale = forms.BooleanField(
        required=False,
        initial=False
    )
    sale_price = forms.DecimalField(
        decimal_places=2,
        max_digits=6,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-lg'})
    )

    class Meta:
        model = Courses
        fields = ['name', 'price', 'description', 'is_sale', 'sale_price', 'new_tags', 'context']