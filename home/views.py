from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ChangeUserDetailsForm
from django.urls import reverse_lazy
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    allPosts = Post.objects.order_by('-views')[:3]
    context = {'allPosts': allPosts}
    return render(request, 'home/home.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        if len(name) < 2:
            messages.error(request, 'Name is too short')
        elif len(email) < 3:
            messages.error(request, 'Email should be more than 3 characters')
        elif len(message) < 10:
            messages.error(request,
                           'Message should be more than 10 characters')
        else:
            contact = Contact(name=name, email=email, message=message)
            contact.save()
            messages.success(request,
                             'Your message has been sent successfully.')
    return render(request, 'home/contact.html')


def about(request):
    return render(request, 'home/about.html')
    
def video(request):
    return render(request, 'home/video.html')


def search(request):
    query = request.GET.get('query')
    if len(query) == 0:
        messages.error(request, "You can't leave the search blank")
        return redirect('home')
    if len(query) > 78:
        allPosts = []
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostContent)
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)


def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        pfp = request.FILES.get('pfp')

        if len(username) > 15:
            messages.error(request,
                           'Username cannot be more than 15 charecters')
            return redirect('home')
        elif len(email) < 3:
            messages.error(request, 'Email should be more than 3 characters')
            return redirect('home')
        elif pass1 != pass2:
            messages.error(request, 'Passwords do not match')
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request,
                             'Your account has been created successfully.')
            form = ProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = myuser
                profile.save()
            return redirect('home')
    else:
        return redirect('home')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['pass']
        user = authenticate(request,
                            username=loginusername,
                            password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('home')
    else:
        return redirect('home')


@login_required
def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ChangeUserDetailsForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below')
            return redirect('profile')
    else:
        form = ChangeUserDetailsForm(instance=request.user)
    return render(request, 'home/profile.html', {'form': form})


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy(
        'password_change')  # Redirects to the same view after success

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully.')
        return super().form_valid(form)


@login_required
def pfp(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST,
                           request.FILES,
                           instance=request.user.profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile photo has been updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below')
    else:
        form = ProfileForm(instance=request.user.profile)

    return render(request, 'home/edit_profile.html', {'form': form})


def error_404_view(request, exception):
    return render(request, 'home/404.html')


def error_500_view(request):
    return render(request, 'home/404.html')
