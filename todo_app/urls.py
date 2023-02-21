from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("login", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("content", views.content, name="content"),
    path("userpage/<int:userid>", views.userpage, name="userpage"),
    path("update/<int:taskid>", views.update, name="update"),
    path("translation/<str:target_content>", views.translation, name="translation"),
    path("delete/<int:id>", views.delete, name="delete")
]