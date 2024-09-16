from django.urls import path
from .views import XeroEmployeeCreateView

urlpatterns = [
    path('create-xero-emp', XeroEmployeeCreateView.as_view(), name='create-xero-employee')
]