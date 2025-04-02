from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from .models import Category,Post,aboutus
import logging
from django.core.paginator import Paginator
from .form import ContactForms, LoginForm, PostForm,registerforms,ForgotForm
from django.contrib import messages
from django.contrib.auth import authenticate , login as auth_login , logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import Group,Permission




def index(request):
    blog_title = "Latest Posts"
    all_posts = Post.objects.filter(is_published=True).order_by('-created_at')  # Ensure ordering
    paginator = Paginator(all_posts, 6)  # Paginate by 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {'blog_title': blog_title, 'page_obj': page_obj})

def details(request, slug):
    if request.user and not request.user.has_perm('blog.view_post'):
        messages.error(request,'You have no permissions to view any posts')
        return redirect('blog:index')
    post = Post.objects.get(slug=slug)
    related_post = Post.objects.filter(category = post.category).exclude(pk=post.id)
    return render(request, "detail.html", {'post': post , 'related_post': related_post})

def old_urls(request):
    return redirect(reverse("blog:new_urls"))

def new_urls(request):
    return HttpResponse("Hello, welcome to the new URL!")               

logger = logging.getLogger("TESTING")

def contact(request):
    if request.method == 'POST':
        form = ContactForms(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        if form.is_valid():
            # Sending the email
            subject = f"Message from {name} - {email}"
            email_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
            send_mail(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,  # Sender email
                ['your_email@example.com'],  # Recipient email (change this to your email)
                fail_silently=False
            )

            # Log the successful sending of the email
            logger.debug(f"Sent email from {email} with message: {message}")
            messages.success(request, "Your email has been sent successfully!")

            # After sending the email, you may want to reset the form fields
            return render(request, "contact.html", {'form': form})

        else:
            logger.debug("Form validation failed")

        return render(request, "contact.html", {'form': form, 'name': name, 'email': email, 'message': message})

    return render(request, "contact.html",)

def about(request):
    about_content = aboutus.objects.first()
    if about_content is None or not about_content.content:
        about_content = "default content is here"
    else:
        about_content = about_content.content
    return render(request,"about.html" , {"about_content":about_content})


def register(request):
    form = registerforms()
    if request.method == 'POST':
        form = registerforms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            # adding user to default group 
            readers_group,created = Group.objects.get_or_create(name='Readers')
            user.groups.add(readers_group)
            messages.success(request,"Resgistration successfull ,You can login now")
            return redirect('blog:login')

    return render(request, 'register.html', {'form': form})


# blog/views.py



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Retrieve the user from the form
            auth_login(request, user)  # Log the user in using the auth_login function
            return redirect('/dashboard/')  # Redirect to the home page after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def dashboard(request):
    tittle = "My Posts"
    all_posts = Post.objects.filter(user=request.user)
    paginator = Paginator(all_posts, 5)  # Paginate by 5 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'dashboard.html', {'tittle':tittle , 'page_obj':page_obj})

def logout(request):
    auth_logout(request)
    return redirect('blog:index')




def forgot_password(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # This will never happen because the form already validated the email.
                messages.error(request, "This email is not registered.")
                return render(request, "forgot_password.html", {'form': form})

            # Generate token and uid
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode('utf-8'))

            # Get the current site domain
            current_site = get_current_site(request)
            domain = current_site.domain

            # Prepare the email content
            subject = "Password Reset Request"
            message = render_to_string('reset_password_email.html', {
                'domain': domain,
                'uid': uid,
                'token': token
            })

            # Send email to the user
            send_mail(subject, message, 'noreply@example.com', [email])

            # Success message
            messages.success(request, "Password reset email sented.")
            return render(request, "forgot_password.html", {'form': form})

    else:
        form = ForgotForm()

    return render(request, "forgot_password.html", {'form': form})



# blog/views.py



def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        messages.error(request, "Invalid link")
        return redirect('forgot_password/')

    if not default_token_generator.check_token(user, token):
        messages.error(request, "Invalid or expired token")
        return redirect('forgot_password/')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been reset successfully!")
            return redirect('/login')
        else:
            messages.error(request, "Passwords do not match")

    return render(request, 'reset_password_form.html', {'uidb64': uidb64, 'token': token})

@login_required
@permission_required('blog.add_post',raise_exception=True)
def new_post(request):
    categories = Category.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('blog:dashboard')

    return render(request,'new_post.html',{'categories':categories , 'form':form})


@login_required
@permission_required('blog.change_post',raise_exception=True)

def edit_post(request,post_id):
    categories = Category.objects.all()
    post = get_object_or_404(Post,id=post_id)
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST , request.FILES,instance=post)
    

        if form.is_valid():
            form.save()
            messages.success(request, "Post Updated Successfully !")

            return redirect('blog:dashboard')

    return render(request,'edit_post.html',{'categories':categories ,'post':post ,'form':form} )
 


@login_required


def delete_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post.delete()
    messages.success(request,'Post Deleted Successfully ')
    return redirect('blog:dashboard')



@login_required
@permission_required('blog.can_publish',raise_exception=True)

def publish_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post.is_published = True
    post.save()
    messages.success(request,'Post had published Successfully')
    return redirect('blog:dashboard')




