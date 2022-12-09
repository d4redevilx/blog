from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from .forms import PostForm
from .models import Post

from django.views.generic import TemplateView, ListView, RedirectView
from django.views import View
from django.utils.decorators import method_decorator


class IndexView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'  # Cambia el `object_list` por un nombre más 'friendly'


class AboutView(TemplateView):
    template_name = 'about.html'


@method_decorator(staff_member_required, name='dispatch')
class CreatePostView(View):
    form_class = PostForm
    template_name = 'create_post.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect('index')
        except ValidationError as e:
            return render(request, self.template_name, {
                'error': e.message
            })


class PostView(View):
    template_name = 'post.html'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['id_post'])
        return render(request, 'post.html', {
            'post': post
        })


@method_decorator(staff_member_required, name='dispatch')
class PostEditView(View):
    template_name = 'edit_post.html'
    form_class = PostForm
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['id_post'])
        return render(request, self.template_name, {
            'post': post
        })

    def post(self, request, *args, **kwargs):
        try:
            post = get_object_or_404(Post, pk=kwargs['id_post'])
            form = self.form_class(request.POST, instance=post)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user
                new_post.save()
                return redirect(self.success_url)
        except ValidationError as e:
            return render(request, self.template_name, {
                'error': e.message
            })


@method_decorator(staff_member_required, name='dispatch')
class PostDeleteView(View):
    redirect_view = 'index'

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['id_post'])
        post.delete()
        return redirect(self.redirect_view)


class SignupView(View):
    template_name = 'signup.html'
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': UserCreationForm
        })

    def post(self, request, *args, **kwargs):
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )

                user.save()

                login(request, user)

                return redirect(self.success_url)
            except IntegrityError:
                return render(request, self.template_name, {
                    'form': UserCreationForm,
                    'error': 'User already exist'
                })

        return render(request, self.template_name, {
            'form': UserCreationForm,
            'error': 'Password do not match'
        })


class SigninView(View):
    template_name = 'signin.html'
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': AuthenticationForm
        })

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, self.template_name, {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })

        login(request, user)
        return redirect(self.success_url)


def signout(request):
    logout(request)
    return redirect('index')
