from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, ht):
    post = get_object_or_404(Post, pk=ht)
    return render(request, 'blog/post_detail.html', {'post': post})
@login_required
def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})
@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', ht=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, ht):
    post = get_object_or_404(Post, pk=ht)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', ht=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


