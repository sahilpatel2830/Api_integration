from logging import exception
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomerSerializer, NestedInvoiceSerializer, EmployeeSerializer, TimeactivitySerializer
from .token_auth import QuickbookAuth
from decouple import config
import requests


class QuickBookBaseView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.auth = QuickbookAuth()
        self.access_token = config('ACCESS_TOKEN')
        self.realm_id = config('REALM_ID')

    def get_header(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

    def send_request(self, url, method, data=None, params=None):
        headers = self.get_header()
        try:
            response = requests.request(method, url, json=data, headers=headers, params=params)
            if response.status_code == 401:
                self.access_token = self.auth.get_new_access_token()
                if not self.access_token:
                    return Response({"error": "Unable to get access token."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                headers = self.get_header()
                response = requests.request(method, url, json=data, headers=headers, params=params)
            return response
        except requests.exceptions.RequestException as request_exception:
            return Response({"message": str(request_exception)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            return Response("Something went wrong. Please try again later", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeCreateView(QuickBookBaseView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee_data = serializer.data

        query = (
            f"SELECT * FROM Employee WHERE GivenName = '{employee_data['GivenName']}' "
            f"AND FamilyName = '{employee_data['FamilyName']}'"
        )
        quickbooks_query_url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/query?minorversion=73'
        query_response = self.send_request(quickbooks_query_url, 'get', params={'query': query})

        if query_response.status_code == 200:
            data = query_response.json()
            if data.get('QueryResponse', {}).get('Employee'):
                return Response({"message": f"Employee with the GivenName {employee_data['GivenName']} and FamilyName {employee_data['FamilyName']} is already exists."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Something went wrong.Please try again later."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        quickbooks_url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/employee?minorversion=73'
        create_emp_response = self.send_request(quickbooks_url, 'post', data=employee_data)

        if create_emp_response.status_code == 200:
            return Response(create_emp_response.json())

        elif create_emp_response.status_code >= 400 and create_emp_response.status_code < 500:
            return Response({"message": "Bad request.","error":create_emp_response.json()}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "Somthing went wrong. Please try again later.","error": create_emp_response.text}, status=status.HTTP_400_BAD_REQUEST)


class BulkEmployeeCreateView(QuickBookBaseView):
    def post(self, request):
        employees = request.data
        if not isinstance(employees, list):
            return Response({"error": "Request data should be list of employee dict."}, status=status.HTTP_400_BAD_REQUEST)

        employee_res = []
        for emp_data in employees:
            serializer = EmployeeSerializer(data=emp_data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validate_emp_data = serializer.data

            quickbooks_url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/employee?minorversion=73'
            create_emp_response = self.send_request(quickbooks_url, 'post', data=validate_emp_data)

            if create_emp_response.status_code == 200:
                employee_info = create_emp_response.json().get("Employee", {})
                employee_res.append({
                    "is_new_emp": True,
                    "GivenName": employee_info.get("GivenName"),
                    "FamilyName": employee_info.get("FamilyName"),
                    "id": employee_info.get("Id")
                })

            elif create_emp_response.status_code == 400:
                create_error_data = create_emp_response.json()
                if "Fault" in create_error_data and "Error" in create_error_data["Fault"]:
                    error_details = create_error_data["Fault"]["Error"][0]

                    if error_details.get("code") == "6240":
                        employee_id = error_details.get("Detail").split("Id=")[-1]

                        employee_res.append({
                            "is_new_emp": False,
                            "GivenName": validate_emp_data.get("GivenName"),
                            "FamilyName": validate_emp_data.get("FamilyName"),
                            "Id": employee_id,
                        })

                    else:
                        employee_res.append({
                            "status": "failed to create",
                            "error": create_error_data
                        })

                else:
                    employee_res.append({
                        "status": "failed to create",
                        "error": employee_res.text
                    })

        return Response(employee_res, status=status.HTTP_200_OK)


class QuickBooksInvoiceCreateView(QuickBookBaseView):
    def post(self, request):
        serializer = NestedInvoiceSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        invoice_data = serializer.data
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/invoice?minorversion=40'
        create_invoice_response = self.send_request(url, 'post', invoice_data)

        if create_invoice_response.status_code == 200:
            return Response(create_invoice_response.json())

        elif create_invoice_response.status_code >= 400 and create_invoice_response.status_code < 500:
            return Response({"message": "Bad request.","error":create_invoice_response.json()}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Something went wrong. Please try again later.","error": create_invoice_response.text}, status=status.HTTP_400_BAD_REQUEST)


class QuickBooksCustomerCreateView(QuickBookBaseView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        customer_data = serializer.data
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/customer?minorversion=73'
        create_customer_response =  self.send_request(url, 'post', customer_data)

        if create_customer_response.status_code == 200:
            return Response(create_customer_response.json())

        elif create_customer_response.status_code >= 400 and create_customer_response.status_code < 500:
            return Response({"message": "Bad request.","error": create_customer_response.json()}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "Somthing went wrong. Please try again later.","error": create_customer_response.text}, status=status.HTTP_400_BAD_REQUEST)


class QuickBookTimeActivity(QuickBookBaseView):
    def post(self, request):
        serializer = TimeactivitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        timeactivity_Data = serializer.data
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/9341452978640153/timeactivity?minorversion=73'
        create_timeactivity_response = self.send_request(url, 'post', timeactivity_Data)

        if create_timeactivity_response.status_code == 200:
            return Response(create_timeactivity_response.json())

        elif create_timeactivity_response.status_code >= 400 and create_timeactivity_response.status_code < 500:
            return Response({"message": "Bad request.","error": create_timeactivity_response.json()})
        else:
            return Response(
                {"message": "Somthing went wrong. Please try again later.", "error": create_timeactivity_response.text},
                status=status.HTTP_400_BAD_REQUEST)


class QuickBooksEmployeeReadView(QuickBookBaseView):
    def get(self, request, employee_id):
        url = f'https://sandbox-quickbooks.api.intuit.com/v3/company/{self.realm_id}/employee/{employee_id}?minorversion=73'
        res = self.send_request(url, 'get')
        if res.status_code == 200:
            return Response({"data": res.json().get("Employee", {}), "message": "Employee details fetched successfully"}, status=status.HTTP_200_OK)
        return Response({"error": res.json()}, status=status.HTTP_200_OK)

