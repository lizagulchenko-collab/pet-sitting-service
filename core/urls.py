from django.shortcuts import redirect
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("pets/", views.PetListView.as_view(), name="pet-list"),
    path("pets/create/", views.PetCreateView.as_view(), name="pet-create"),
    path("pets/<int:pk>/", views.PetDetailView.as_view(), name="pet-detail"),
    path(
        "pets/<int:pk>/update/",
        views.PetUpdateView.as_view(),
        name="pet-update",
    ),
    path(
        "pets/<int:pk>/delete/",
        views.PetDeleteView.as_view(),
        name="pet-delete",
    ),
    path("bookings/", views.BookingListView.as_view(), name="booking-list"),
    path(
        "bookings/create/",
        views.BookingCreateView.as_view(),
        name="booking-create",
    ),
    path("", lambda request: redirect("login"), name="home"),
    path("register/", views.client_register_view, name="register"),
    path("login/", views.client_login_view, name="login"),
    path("logged_out/", views.client_logout_view, name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path(
        "animal-types/",
        views.AnimalTypeListView.as_view(),
        name="animaltype-list",
    ),
    path(
        "animal-types/create/",
        views.AnimalTypeCreateView.as_view(),
        name="animaltype-create",
    ),
]
