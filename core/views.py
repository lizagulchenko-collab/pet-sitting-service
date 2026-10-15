from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (TemplateView,
                                  ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)

from .forms import (BookingForm,
                    ClientLoginForm,
                    ClientRegistrationForm,
                    PetForm,
                    AnimalTypeForm)
from .models import Booking, Pet, Animal


class IndexView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["num_pets"] = Pet.objects.filter(
                pet_parent=self.request.user
            ).count()
            context["num_bookings"] = Booking.objects.filter(
                pet_id__pet_parent=self.request.user
            ).count()
        return context


def client_register_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:index")
    else:
        form = ClientRegistrationForm()

    return render(request, "registration/login.html", {"form": form})


class PetListView(LoginRequiredMixin, ListView):
    model = Pet
    template_name = "core/pet_list.html"
    context_object_name = "pet_list"
    paginate_by = 5

    def get_queryset(self):
        return Pet.objects.filter(pet_parent=self.request.user)


class PetDetailView(LoginRequiredMixin, DetailView):
    model = Pet
    template_name = "core/pet_detail.html"
    context_object_name = "pet"

    def get_queryset(self):
        return Pet.objects.filter(pet_parent=self.request.user)


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    template_name = "core/pet_form.html"
    success_url = reverse_lazy("core:pet-list")

    def form_valid(self, form):
        form.instance.pet_parent = self.request.user
        return super().form_valid(form)


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "core/pet_form.html"
    success_url = reverse_lazy("core:pet-list")

    def get_queryset(self):
        return Pet.objects.filter(pet_parent=self.request.user)


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = "core/pet_confirm_delete.html"
    success_url = reverse_lazy("core:pet-list")

    def get_queryset(self):
        return Pet.objects.filter(pet_parent=self.request.user)


class AnimalTypeListView(LoginRequiredMixin, ListView):
    model = Animal
    template_name = "core/animaltype_list.html"
    context_object_name = "animal_types"


class AnimalTypeCreateView(LoginRequiredMixin, CreateView):
    model = Animal
    form_class = AnimalTypeForm
    template_name = "core/animaltype_form.html"
    success_url = reverse_lazy("core:animaltype-list")


class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = "core/booking_list.html"
    context_object_name = "booking_list"
    paginate_by = 5

    def get_queryset(self):
        return Booking.objects.filter(pet_id__pet_parent=self.request.user)


class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = "core/booking_form.html"
    success_url = reverse_lazy("core:booking-list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


def client_register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account created")
            return redirect("dashboard")
        else:
            messages.error(request, "Please, enter correct information")
    else:
        form = ClientRegistrationForm()

    return render(request, "core/register.html", {"form": form})


def client_login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = ClientLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name}!")
            return redirect("dashboard")
        else:
            messages.error(request, "Incorrect email or password")
    else:
        form = ClientLoginForm()

    return render(request, "core/login.html", {"form": form})


def client_logout_view(request):
    logout(request)
    messages.info(request, "You logged out")
    return redirect("login")


@login_required
def dashboard_view(request):
    user = request.user

    pets = Pet.objects.filter(pet_parent=user)
    bookings = Booking.objects.filter(pet_id__pet_parent=user)

    pet_form = PetForm(prefix="pet")
    booking_form = BookingForm(user=user, prefix="booking")

    if request.method == "POST":
        if "submit_pet" in request.POST:
            pet_form = PetForm(request.POST, prefix="pet")
            if pet_form.is_valid():
                pet = pet_form.save(commit=False)
                pet.pet_parent = user
                pet.save()
                messages.success(request, f"Pet {pet.name} successfully added")
                return redirect("dashboard")

        elif "submit_booking" in request.POST:
            booking_form = BookingForm(request.POST, user=user, prefix="booking")
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)

                days = (booking.end_date - booking.start_date).days
                days = max(days, 1)
                booking.total_price = days * 300

                booking.save()
                messages.success(request, "Order created")
                return redirect("dashboard")

    context = {
        "pets": pets,
        "bookings": bookings,
        "pet_form": pet_form,
        "booking_form": booking_form,
    }
    return render(request, "core/dashboard.html", context)
