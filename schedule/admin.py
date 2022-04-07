from django.contrib import admin

from .models import Address, Employee, Establishment, Faithfulness, Scheduling


@admin.register(Scheduling)
class SchedulingAdmin(admin.ModelAdmin):
    list_display = (
        "provider",
        "client_name",
        "client_email",
        "client_phone",
        "date_time",
        "states",
        "confirmed",
        "canceled",
    )  # noqa:E501


@admin.register(Faithfulness)
class FaithfulnessAdmin(admin.ModelAdmin):
    list_display = ("provider", "client", "level")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("provider", "establishment", "assignment")


@admin.register(Establishment)
class EstablishmentAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "establishment",
        "cep",
        "city",
        "district",
        "street",
        "complement",
    )  # noqa:E501
