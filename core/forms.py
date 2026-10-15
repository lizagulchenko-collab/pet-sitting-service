from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Booking, Pet, Animal

User = get_user_model()


class ClientLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@email.com",
                "autofocus": True,
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your password",
            }
        ),
    )


class ClientRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "country",
            "city",
        )
        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "example@email.com",
                }
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "First name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Last name"}
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+380XXXXXXXXX",
                }
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Country"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City"}
            ),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CLIENT
        if commit:
            user.save()
        return user


class AnimalTypeForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Example: cat, dog, rat"}
            ),
        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = (
            "name",
            "animal",
            "age",
            "allergies",
            "training_required",
            "walk_times",
            "additional_info",
        )
        labels = {
            "name": "Name",
            "animal": "Animal type",
            "age": "Age",
            "allergies": "Allergies (if any)",
            "training_required": "Training required",
            "walk_times": "Walk times",
            "additional_info": "Additional information",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "animal": forms.Select(attrs={"class": "form-select"}),
            "age": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}
            ),
            "allergies": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Allergies",
                }
            ),
            "training_required": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "walk_times": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}
            ),
            "additional_info": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What else pet sitter should know",
                }
            ),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("pet", "staff", "start_date", "end_date")
        labels = {
            "pet": "Choose your pet",
            "staff": "Choose staff you like",
            "start_date": "Start date",
            "end_date": "End date",
        }
        widgets = {
            "pet": forms.Select(attrs={"class": "form-select"}),
            "staff": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["pet"].queryset = Pet.objects.filter(pet_parent=user)