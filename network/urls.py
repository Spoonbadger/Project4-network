
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("new_post/", views.new_post, name="new_post"),
    path("all_posts/", views.all_posts, name="all_posts"),
    path("like_unlike/<int:post_id>/", views.like_unlike, name="like_unlike"),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path('profile/<int:user_id>/', views.profile, name="profile"),
    path('api/profile/<int:user_id>/', views.profile_data, name="profile_data"),
    path('following_posts/', views.following_posts, name="following_posts"),
    path('api/following_posts/', views.following_posts_data, name="following_posts_data"),
    path('follow_unfollow/<int:user_id>/', views.follow_unfollow, name="follow_unfollow"),
    path('<int:post_id>/delete/', views.delete_squeek, name="delete_squeek"),
    path('delete_account/<int:user_id>/', views.delete_account, name="delete_account")
]
