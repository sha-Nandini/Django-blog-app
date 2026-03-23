from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Blog, Comment
from .forms import BlogForm, CommentForm, SignUpForm


def home(request):
    blogs = Blog.objects.all().order_by('-timestamp')
    return render(request, 'home.html', {'blogs': blogs})


@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('home')
    else:
        form = BlogForm()

    return render(request, 'create.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def read_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    comments = blog.comments.all()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.user = request.user
                comment.save()
                return redirect('read', id=id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'read.html', {
        'blog': blog,
        'comments': comments,
        'form': form
    })


@login_required
def edit_blog(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.author != request.user and not request.user.is_superuser:
        return redirect('home')

    if request.method == 'POST':
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'create.html', {'form': form})



@login_required
def delete_blog(request, id):
    blog = get_object_or_404(Blog, id=id)


    if blog.author != request.user and not request.user.is_superuser:
        return redirect('home')

    if request.method == "POST":
        blog.delete()
        return redirect('home')


    return render(request, "delete.html", {"blog": blog})

    