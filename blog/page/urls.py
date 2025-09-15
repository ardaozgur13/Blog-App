from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("post/<int:pk>", views.post, name="post"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("signup/", views.signup_user, name="signup"),
    path("update_user/", views.update_user, name="update_user"),
    path("update_password/", views.update_password, name="update_password"),
    path("update_info", views.update_info, name="update_info"),
    path("add_post", views.add_post, name="add_post"),
    path("search_tag", views.search_tag, name="search_tag"),
    path("search_user", views.search_user, name="search_user"),
    path("tag/<str:tag_item>", views.tag, name="tag"),
    path("user_profile_page/<str:username>", views.user_profile_page, name="user_profile_page"),
]