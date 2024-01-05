from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from .models import Posts


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
    else:
        form = PostForm(data=request.GET)
    
    return render(request, 'posts/create.html', {'form': form})

def feed(request):
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        new_comment = comment_form.save(commit=False)
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Posts, id=post_id)
        new_comment.post = post
        new_comment.save()
    else:
        comment_form = CommentForm()

    posts = Posts.objects.all()
    logged_user = request.user
    return render(request, 'posts/feed.html', {'posts': posts, 'logged_user': logged_user, 'comment_form': comment_form})



def like_post(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Posts, id=post_id)
    if post.liked_by.filter(id=request.user.id).exists():
        post.liked_by.remove(request.user)
    else:
        post.liked_by.add(request.user)
    
    return redirect('feed')
