from django.urls import path
from .views import (EmployeeCreateView, QuickBooksInvoiceCreateView, QuickBooksCustomerCreateView,
                     QuickBookTimeActivity, QuickBooksEmployeeReadView, BulkEmployeeCreateView)

urlpatterns = [
    path('create-employee/', EmployeeCreateView.as_view(), name='employee-create'),
    path('bulk-create-employee/',BulkEmployeeCreateView.as_view(), name='bulk-create-employee'),
    path('create-invoice/', QuickBooksInvoiceCreateView.as_view(), name='invoice-create'),
    path('create-customer/', QuickBooksCustomerCreateView.as_view(), name='customer-create'),
    path('create-timeactivity/', QuickBookTimeActivity.as_view(), name='timeactivity-create'),
    path('read-employee/<int:employee_id>/', QuickBooksEmployeeReadView.as_view(), name='read-employee'),

]
