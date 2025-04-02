from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from blog.models import Category,Post
from .models import Post 



class ContactForms(forms.Form):
    name = forms.CharField(label="name",max_length=100,required=True)
    email = forms.EmailField(label="email" , required=True)
    message = forms.CharField(label="message" , required=True)




class registerforms(forms.ModelForm):
    username = forms.CharField(label="Username", max_length=100, required=True)
    email = forms.EmailField(label="Email", max_length=100, required=True)
    password = forms.CharField(label="Password", max_length=100, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", max_length=100, required=True, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
    class Meta:
        model = User
        fields= ['username' , 'email' , 'password']


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput, max_length=100, required=True)


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid User and password ")
            



class ForgotForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100, required=True)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError("No user registered with this email.")
        return email
    

class PostForm(forms.ModelForm):
    title = forms.CharField(label="title", max_length=100, required=True)
    content = forms.CharField(label="content", max_length=100, required=True)
    category = forms.ModelChoiceField(label="category",  required=True , queryset = Category.objects.all())
    image_url = forms.ImageField(label="image",required=False)

    class Meta:
        model = Post
        fields = ['title','content','category','image_url']

    def clean(self):
        cleaned_data = super().clean() 
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and len(title) <5:
            raise forms.ValidationError('Title must be atleast 5 characters long')
        if content and len(content) <10:
            raise forms.ValidationError('content must be 10 charcaters long')

    def save(self, commit = ...):
        post = super().save(commit)
        cleaned_data = super().clean()

        if cleaned_data.get('image_url'):
            post.image_url = cleaned_data.get('image_url')
        else:
            img_url = "post/media/images.jpg"
            post.image_url = img_url

        if commit:
            post.save()
        return post
