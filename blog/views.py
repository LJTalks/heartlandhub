from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic
from django.contrib import messages
from .models import Post, Comment
from django.http import HttpResponseRedirect
from .forms import CommentForm

# Create your views here.


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "blog/post_list.html"
    paginate_by = 6


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.
    **Context**
    ``post``
        An instance of :model:`blog.Post`.
    **Template:**

    :template:`blog/post_detail.html`
    """

    queryset = Post.objects.filter(status=1)
    # Get the current post
    post = get_object_or_404(queryset, slug=slug)
    # Get the previous post
    previous_post = Post.objects.filter(
        created_on__lt=post.created_on, status=1).order_by(
            '-created_on').first()
    # Get the next post
    next_post = Post.objects.filter(
        created_on__gt=post.created_on, status=1).order_by(
            'created_on').first()
        
    # Comments
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()

    if request.method == "POST":
        print("received a POST request")
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.add_message(
                request, messages.SUCCESS, "Comment submitted and awaiting approval"
            )

    comment_form = CommentForm()
    print("about to render template")

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "previous_post": previous_post,
            "next_post": next_post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
        },
    )
