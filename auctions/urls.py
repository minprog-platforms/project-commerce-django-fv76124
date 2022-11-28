from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addlisting", views.addlisting, name="addlisting"),
    path("activelisting/<int:id>", views.activelisting, name="activelisting"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("closedlisting<int:id>", views.closedlisting, name="closedlisting")
    ]