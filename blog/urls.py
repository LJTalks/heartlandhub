from django.urls import path
from . import views


urlpatterns = [
    # this is the blog home page that has all the blogs
    # The blog home page/list view
    # Not sure where this came from
    # It's a view in blogs, move to Profile when it exists
    path('unsubscribe/<int:user_id>/', views.unsubscribe, name='unsubscribe'),
    # Individual Blog posts with slug address
    path("blog/", views.PostList.as_view(), name="blog"),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path(
        "<slug:slug>/edit_blog_comment/<int:blog_comment_id>",
        views.blog_comment_edit,
        name="blog_comment_edit",
    ),
    path(
        "<slug:slug>/delete_blog_comment/<int:blog_comment_id>",
        views.blog_comment_delete,
        name="blog_comment_delete",
    ),
]
