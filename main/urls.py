from django.urls import path
from . import views

urlpatterns = [
    path("", views.root),
    path("register", views.register),
    path("login", views.login),
    path("dashboard", views.dashboard),
    path("logout", views.logout),
    path("wishes/new", views.new_wish),
    path("create_wish", views.create_wish),
    path("delete/<int:id>", views.delete_wish),
    path("edit/<int:id>", views.edit_wish),
    path("update/<int:id>", views.update_wish),
    path("wishes/stats", views.wish_info), 
    path("like/<int:id>", views.like_wish),
    path("cancel/<int:id>", views.cancel_wish),
]