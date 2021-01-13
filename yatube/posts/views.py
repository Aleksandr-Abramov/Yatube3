from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Post
from .models import Group
from .models import User

from .forms import PostForm
from .forms import FormComments


def index(request):
    """Главная страница Index"""
    post_list = Post.objects.select_related("group")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page
    }
    return render(request, "index.html", context)


def group_posts(request, slug):
    """Страница записей сообщества group_post"""
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    context = {
        "post": posts,
        "group": group,
    }
    return render(request, "group.html", context)


@login_required
def new_post(request):
    """Страница создание поста new"""
    if request.method != "POST":
        form = PostForm()
        context = {
            "form": form
        }
        return render(request, "add_or_change_post.html", context)

    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect("index")


def profile(request, username):
    """Профайл пользователя User and Post"""
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "user": user,
        "page": page,
    }
    return render(request, "profile.html", context)


def post_view(request, username, post_id):
    """Просмотр записи Post"""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    author_posts = post.author
    comments = post.comments.all()
    form = FormComments()
    context = {
        "author_posts": author_posts,
        "post": post,
        "form": form,
        "comments": comments
    }
    return render(request, "post.html", context)


@login_required
def post_edit(request, username, post_id):
    """Страница редактирования поста post_edit"""
    profile = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, pk=post_id, author=profile)

    if request.user != profile:
        return redirect('post', username=username, post_id=post_id)

    if request.method != "POST":
        form = PostForm(instance=post)
        context = {
            "form": form,
            "is_edit": True,
        }
        return render(request, 'add_or_change_post.html', context)

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("post", username=request.user.username, post_id=post_id)


def add_comment(request, username, post_id):
    """Форма комментариев"""
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=request.user)

    if request.method != "POST":
        form = FormComments()
        context = {
            "form": form
        }
        return render(request, "includes/comments.html", context)

    form = FormComments(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = author
        comment.save()
        return redirect("post", username=username, post_id=post_id)


def page_not_found(request, exception):
    """Страница ошибки 404"""
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    """Страница ошибки 500"""
    return render(request, "misc/500.html", status=500)
