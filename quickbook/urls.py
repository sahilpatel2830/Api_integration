from django.urls import path
from .views import (EmployeeCreateView, QuickBooksInvoiceCreateView, QuickBooksCustomerCreateView,
                     QuickBookTimeActivity, QuickBooksEmployeeReadView, SyncEmployeeCreateView,
                    SyncCustomerCreateView)

urlpatterns = [
    path('create-employee/', EmployeeCreateView.as_view(), name='employee-create'),
    path('sync-employees/',SyncEmployeeCreateView.as_view(), name='sync-employees'),
    path('create-invoice/', QuickBooksInvoiceCreateView.as_view(), name='invoice-create'),
    path('create-customer/', QuickBooksCustomerCreateView.as_view(), name='customer-create'),
    path('sync-customers/', SyncCustomerCreateView.as_view(), name='sync-customers'),
    path('create-timeactivity/', QuickBookTimeActivity.as_view(), name='timeactivity-create'),
    path('read-employee/<int:employee_id>/', QuickBooksEmployeeReadView.as_view(), name='read-employee'),

]
