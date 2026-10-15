from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from core.models import Animal, Pet


class AnimalTypeNameValidationTests(TestCase):
    def test_animal_type_name_not_empty(self):
        animal_type = Animal(name="")
        with self.assertRaises(ValidationError):
            animal_type.full_clean()


class PublicAccessTests(TestCase):
    def test_index_page_accessible_for_anonymous_user(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)

    def test_pet_list_login_required(self):
        response = self.client.get(reverse("core:pet-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_booking_list_login_required(self):
        response = self.client.get(reverse("core:booking-list"))
        self.assertNotEqual(response.status_code, 200)

    def test_animal_type_list_login_required(self):
        response = self.client.get(reverse("core:animaltype-list"))
        self.assertNotEqual(response.status_code, 200)


class SearchAndListTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="petowner@mail.com",
            password="testpass123",
            phone_number="+380991112233",
        )
        self.client.force_login(self.user)

        self.dog_type = Animal.objects.create(name="Dog")
        self.rat_type = Animal.objects.create(name="Rat")

        self.pet1 = Pet.objects.create(
            name="Archi",
            animal=self.dog_type,
            age=3,
            pet_parent=self.user,
        )
        self.pet2 = Pet.objects.create(
            name="Tory",
            animal=self.rat_type,
            age=2,
            pet_parent=self.user,
        )

    def test_animal_type_list_contains_types(self):
        response = self.client.get(reverse("core:animaltype-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dog")
        self.assertContains(response, "Rat")

    def test_pet_list_shows_only_user_pets(self):
        other_user = get_user_model().objects.create_user(
            email="otheruser@gmail.com",
            password="testpass123",
            phone_number="+380992223344",
        )
        Pet.objects.create(
            name="Ray",
            animal=self.dog_type,
            age=5,
            pet_parent=other_user,
        )

        response = self.client.get(reverse("core:pet-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Archi")
        self.assertContains(response, "Tory")
        self.assertNotContains(response, "Ray")

    def test_booking_list_access(self):
        response = self.client.get(reverse("core:booking-list"))
        self.assertEqual(response.status_code, 200)


class DashboardContextTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="dashboard_user@mail.com",
            password="testpass123",
            phone_number="+380993334455",
        )
        self.client.force_login(self.user)

        self.dog_type = Animal.objects.create(name="Dog")
        self.pet = Pet.objects.create(
            name="Donut",
            animal=self.dog_type,
            age=4,
            pet_parent=self.user,
        )

    def test_dashboard_num_pets_counter(self):
        response = self.client.get(reverse("core:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_pets"], 1)
