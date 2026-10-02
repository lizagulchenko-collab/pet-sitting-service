from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff, User


class StaffInline(admin.StackedInline):
    model = Staff
    can_delete = False
    verbose_name_plural = "Staff"
    fk_name = "user"


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (StaffInline,)

    list_display = ("email",
                    "first_name",
                    "last_name",
                    "role",
                    "is_staff",
                    "phone_number",
                    "country",
                    "city")
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone_number")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("first_name",
                        "last_name",
                        "role",
                        "phone_number",
                        "country",
                        "city")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "country",
                    "city"
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

