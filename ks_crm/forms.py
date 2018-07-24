# -*- coding: utf-8 -*-
__author__ = 'Allen'

from django import forms
from django.forms import widgets
from ks_crm.models import UserProfile
from ks_edu import settings
try:
    from string import letters
except ImportError:
    from string import ascii_letters as letters
from string import punctuation, digits
from .send_emails import generate_activation_key
import pytz # $ pip install pytz
from tzlocal import get_localzone # $ pip install tzlocal

UNAME_CHARS = letters + "._" + digits
PWD_CHARS = letters + punctuation + digits

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=30, help_text='Letters, digits,\
                    period and underscores only.')
    email = forms.EmailField()
    password = forms.CharField(max_length=30, widget=forms.PasswordInput())
    confirm_password = forms.CharField(
        max_length=30, widget=forms.PasswordInput())



    # def clean_username(self):
    #     u_name = self.cleaned_data["username"]
    #     if u_name.strip(UNAME_CHARS):
    #         msg = "Only letters, digits, period and underscore characters are" \
    #               " allowed in username"
    #         raise forms.ValidationError(msg)
    #     try:
    #         UserProfile.objects.get(username__exact=u_name)
    #         raise forms.ValidationError("Username already exists.")
    #     except UserProfile.DoesNotExist:
    #         return u_name

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if pwd.strip(PWD_CHARS):
            raise forms.ValidationError("Only letters, digits and punctuation\
                                            are allowed in password")
        return pwd

    def clean_confirm_password(self):
        c_pwd = self.cleaned_data['confirm_password']
        pwd = self.data['password']
        if c_pwd != pwd:
            raise forms.ValidationError("Passwords do not match")

        return c_pwd

    def clean_email(self):
        user_email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=user_email).exists():
            raise forms.ValidationError("This email already exists")
        return user_email

    def save(self):
        u_name = self.cleaned_data["name"]
        pwd = self.cleaned_data["password"]
        email = self.cleaned_data['email']
        new_user = UserProfile.objects.create_user(email, u_name, pwd)
        new_user.save()

        return u_name, pwd, new_user.email

class ProfileForm(forms.Form):
    # from ks_crm.models import Course
    # course_list = Course.objects.filter(enabled=True)
    # course_choices = [(course.id,course.name) for course in course_list]
    email = forms.EmailField(widget=widgets.TextInput(attrs={'class':'form-control','readonly':'readonly'}))
    name = forms.CharField(widget=widgets.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(widget=widgets.TextInput(attrs={'class':'form-control','readonly':'readonly'}))
    true_name = forms.CharField(widget=widgets.TextInput(attrs={'class':'form-control'}),required=False)
    stu_num = forms.IntegerField(widget=widgets.TextInput(attrs={'class':'form-control'}),required=False)
    grade = forms.IntegerField(widget=widgets.Select(choices=[('1', '大一'), ('2', '大二'), ('3', '大三'), ('4', '大四')],attrs={'class':'form-control'}))
    degree = forms.IntegerField(widget=widgets.Select(choices=[('0', '专科'), ('1', '本科')],attrs={'class':'form-control'}))
    isteacher = forms.IntegerField(widget=widgets.Select(choices=[('0', '是'), ('1', '否')],attrs={'class':'form-control'}))
    ismakeup = forms.IntegerField(widget=widgets.Select(choices=[('0', '是'), ('1', '否')],attrs={'class':'form-control'}))
    gender = forms.IntegerField(widget=widgets.Select(choices=[('0', '男'), ('1', '女')],attrs={'class':'form-control'}))
    profession = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),required=False)
    role = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    signature = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),required=False)
    address = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),required=False)
    hobbies = forms.CharField(widget=widgets.TextInput(attrs={'class': 'form-control'}),required=False)
    phone = forms.IntegerField(widget=widgets.NumberInput(attrs={'class': 'form-control'}),required=False)
    ID_num = forms.IntegerField(widget=widgets.NumberInput(attrs={'class': 'form-control'}),required=False)
    # course = forms.MultipleChoiceField(widget=widgets.SelectMultiple(attrs={'class': 'form-control'}),choices=course_choices,disabled=True)

