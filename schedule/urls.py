from django.urls import path

from .views import (
    AddressDetail,
    AddressList,
    EmployeeDetail,
    EmployeeEstablishmentList,
    EmployeeList,
    EstablishmentAddressList,
    EstablishmentDetail,
    EstablishmentList,
    HoraryList,
    SchedulingDetail,
    SchedulingList,
    healthcheck,
    report_providers,
    user_functions,
)

urlpatterns = [
    path("", healthcheck),
    path("scheduling/", SchedulingList.as_view()),
    path("scheduling/<int:id>/", SchedulingDetail.as_view()),
    path("horary/<str:date>/", HoraryList.as_view()),
    path("providers/", report_providers),
    path("establishment/", EstablishmentList.as_view()),
    path("establishment/<int:id>/", EstablishmentDetail.as_view()),
    path("employee/", EmployeeList.as_view()),
    path("employee/<int:id>/", EmployeeDetail.as_view()),
    path("employee_establishment/", EmployeeEstablishmentList.as_view()),
    path("address/", AddressList.as_view()),
    path("address/<int:id>/", AddressDetail.as_view()),
    path("establishment_address/", EstablishmentAddressList.as_view()),
    path("users/", user_functions),
]
