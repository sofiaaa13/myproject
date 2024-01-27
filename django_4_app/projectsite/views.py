from django.http import JsonResponse
from .models import User, Follow, Post, Comment
from django.views.generic.base import TemplateView
from .forms import RegistrationForm, LoginForm, SearchForm, CommentForm, AddPostForm
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.template.loader import render_to_string
from pathlib import Path
from django.core.files import File


class ProfilePage(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        user = self.request.user
        follow = Follow.objects.get(user=user)
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile {user}'.format(user=user.username)
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['post_am'] = len(Post.objects.filter(user=user))
        context['followers'] = len(follow.followers.all())
        context['following'] = len(follow.following.all())
        return context


class UserProfileView(TemplateView):
    template_name = 'user_profile.html'

    def post(self, request, **kwargs):
        data_post = request.POST
        current_user = self.request.user
        current_user_follow = Follow.objects.get(user=current_user)
        f_user = Follow.objects.get(user=User.objects.get(id=data_post['follow']))
        if data_post['is_followed'] == '0':
            current_user_follow.following.add(User.objects.get(id=data_post['follow']))
            current_user_follow.save()
            f_user.followers.add(current_user)
            f_user.save()
            return JsonResponse({'is_follow': 1, 'followers': len(f_user.followers.all())})
        else:
            current_user_follow.following.remove(User.objects.get(id=data_post['follow']))
            current_user_follow.save()
            f_user.followers.remove(current_user)
            f_user.save()
            return JsonResponse({'is_follow': 0, 'followers': len(f_user.followers.all())})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        current_user_follow = Follow.objects.get(user=current_user)
        user = User.objects.get(id=self.kwargs['pk'])
        context['is_followed'] = 1
        if user not in current_user_follow.following.all():
            context['is_followed'] = 0
        context['title'] = user.username
        context['followers'] = len(current_user_follow.followers.all())
        context['following'] = len(current_user_follow.following.all())
        context['current_user'] = current_user
        context['user'] = user
        context['posts'] = Post.objects.filter(user=user)
        context['post_am'] = len(Post.objects.filter(user=user))
        return context



class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context
    def get_success_url(self):
        follow = Follow(user=self.object)
        follow.save()
        return '/login'


class Login(LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    extra_context = {'title': 'Log In'}
    form_class = LoginForm


class HomeView(CreateView):
    template_name = 'home.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        post_data = request.POST
        user = self.request.user

        if 'id' in post_data.keys():
            post = Post.objects.get(id=post_data['id'])
            context = {}
            comments = Comment.objects.filter(post=post)
            context['comments'] = comments
            context['profile'] = user
            context['form'] = CommentForm()
            response = render_to_string('post.html', context)
            return JsonResponse(response, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user


        posts = Post.objects.all()
        context['posts'] = posts
        context['title'] = 'Home'
        context['user'] = user

        return context


class AddPostView(TemplateView):
    model = Post
    template_name = 'add_post.html'
    form_class = AddPostForm

    def post(self, request):
        data = request.POST
        if len(data.keys()) == 1:
            data = request.FILES['file']
            with open('media/static/images/upload_image.png', 'wb') as file:
                file.write(data.read())
        else:
            description = data['description']
            path = Path('media/static/images/upload_image.png')
            with path.open(mode='rb') as f:
                file = File(f, name=path.name)
                post = Post(text=description, photo=file, user=self.request.user)
                post.save()
        return JsonResponse('media/static/images/upload_image.png', safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Post'
        return context


class SearchView(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        data_post = self.request.POST
        users = User.objects.filter(username__contains=data_post['input'])
        result = render_to_string('search_results_template.html', {'results': users})
        return JsonResponse(result, safe=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search'
        context['profile'] = self.request.user
        return context


class Logout(LogoutView):
    pass


