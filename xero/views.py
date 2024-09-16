from quickbooks.objects import Employee
from rest_framework.response import Response
from rest_framework.views import APIView
from xero_python.api_client import ApiClient, Configuration
from xero_python.accounting import AccountingApi
from rest_framework import status
from xero_python.payrollau import Employees
from xero_python.api_client.oauth2 import OAuth2Token
from .serializers import XeroEmployeeSerializer
from xero_python.exceptions import AccountingBadRequestException


class XeroEmployeeCreateView(APIView):
    def post(self, request):
        api_client = ApiClient(
            Configuration(
                debug=False,
                oauth2_token=OAuth2Token(
                    client_id="D3C511D34CD74C9C83544F5A20C22432",
                    client_secret="x_cJ5_LIqtssLOInWpGkP2BbhCjPPhMgo0MxZWfG9enBStQR"
                ),
            ),
            pool_threads=1,
        )

        api_client.set_oauth2_token(
            token={
                "xero-tenant-id": "45d3352a-1557-4787-b0a1-d2827a8dd9fc",
                "access_token": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjFDQUY4RTY2NzcyRDZEQzAyOEQ2NzI2RkQwMjYxNTgxNTcwRUZDMTkiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJISy1PWm5jdGJjQW8xbkp2MENZVmdWY09fQmsifQ.eyJuYmYiOjE3MjYwNTEyMjgsImV4cCI6MTcyNjA1MzAyOCwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS54ZXJvLmNvbSIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHkueGVyby5jb20vcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiRDNDNTExRDM0Q0Q3NEM5QzgzNTQ0RjVBMjBDMjI0MzIiLCJzdWIiOiIyY2ZlNmQ5MWE1NWE1YWJjODM3YWU4MTE4MzVlM2ZkZSIsImF1dGhfdGltZSI6MTcyNjA1MTIxOSwieGVyb191c2VyaWQiOiI5MTY5ZjllYi1kMzBjLTRlMDItYjI0Yi04NTViZTc0ZWUwZjEiLCJnbG9iYWxfc2Vzc2lvbl9pZCI6ImM5OTlkMDUzZDEyODQwOGJiZGNjYWY3MzgwMzYzMmY0Iiwic2lkIjoiYzk5OWQwNTNkMTI4NDA4YmJkY2NhZjczODAzNjMyZjQiLCJqdGkiOiIxRkIyOUNFNTBFM0I0NjkxOTMwMjcxMDAzNDVBQ0M0OSIsImF1dGhlbnRpY2F0aW9uX2V2ZW50X2lkIjoiYmFjZjcwNDItZjhmYi00Yzc5LThkOGYtYjg1MTJiZWQwMGU1Iiwic2NvcGUiOlsiZW1haWwiLCJwcm9maWxlIiwib3BlbmlkIiwiYWNjb3VudGluZy50cmFuc2FjdGlvbnMiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsicHdkIl19.HcVBDmJoOwNd0lh4kpDGN7y0f7thKpIdHLnbJwPPsdaTCmqSCUVTCMRmQIBMzS4Fv-UUGimbQuYSufFoJ3chJ9OzIC5bNc2zOl5UFnCRhS9a__CIwTMVPWka03disEVBhSAxox23CakKfJT3rYHEJaZFIq2fcTjtNdWGM5DXZ9o6_jPli1LWoy3Cw-PTJT2w0vfA5qGsJGX9SlafF2ABGmvDyyAHAR23livRnUMUPR_il3IVV8WONx48QVYQ5gExMQTRcDyxVTq-ZMcv0B2F1Q-6wZauTa9_DOPGL4uD8b3SRCtDJBq6pG8YjodB2GRvAuqStq7QobN6oobmYTDQfg"}
        )

        api_instance = AccountingApi(api_client)

        xero_tenant_id = '45d3352a-1557-4787-b0a1-d2827a8dd9fc'
        serializer = XeroEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        employee_data = serializer.validated_data
        employee = Employee(
            first_name=employee_data.get('FirstName'),
            last_name=employee_data.get('LastName')
        )
        employees = Employees(
            employees=[employee]
        )

        try:
            api_response = api_instance.create_employees(
                xero_tenant_id,
                employees,
                summarize_errors=True,
                idempotency_key='KEY_VALUE'
            )
            return Response(api_response.to_dict(), status=status.HTTP_201_CREATED)
        except AccountingBadRequestException as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class XeroEmployeeCreateView(APIView):
#     def post(self,request):
#         XERO_API_URL = "https://api.xero.com/api.xro/2.0/Employees"
#         XERO_API_TOKEN = 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjFDQUY4RTY2NzcyRDZEQzAyOEQ2NzI2RkQwMjYxNTgxNTcwRUZDMTkiLCJ0eXAiOiJKV1QiLCJ4NXQiOiJISy1PWm5jdGJjQW8xbkp2MENZVmdWY09fQmsifQ.eyJuYmYiOjE3MjU5NTcyNzAsImV4cCI6MTcyNTk1OTA3MCwiaXNzIjoiaHR0cHM6Ly9pZGVudGl0eS54ZXJvLmNvbSIsImF1ZCI6Imh0dHBzOi8vaWRlbnRpdHkueGVyby5jb20vcmVzb3VyY2VzIiwiY2xpZW50X2lkIjoiRDNDNTExRDM0Q0Q3NEM5QzgzNTQ0RjVBMjBDMjI0MzIiLCJzdWIiOiIyY2ZlNmQ5MWE1NWE1YWJjODM3YWU4MTE4MzVlM2ZkZSIsImF1dGhfdGltZSI6MTcyNTk1NzI1NiwieGVyb191c2VyaWQiOiI5MTY5ZjllYi1kMzBjLTRlMDItYjI0Yi04NTViZTc0ZWUwZjEiLCJnbG9iYWxfc2Vzc2lvbl9pZCI6IjFiNzRkNGM2NjlmZjRlNDVhYzBhYzMxMzZjYzU2YWViIiwic2lkIjoiMWI3NGQ0YzY2OWZmNGU0NWFjMGFjMzEzNmNjNTZhZWIiLCJqdGkiOiJBQzk0NzUzRTJCMTUxRjAxOUI2QjcwNEFENDk3MjdBOSIsImF1dGhlbnRpY2F0aW9uX2V2ZW50X2lkIjoiY2VhNTYxNmEtOTliYi00YTc3LThmMTAtYWNmMDgxOTdhNDk2Iiwic2NvcGUiOiJhY2NvdW50aW5nLnRyYW5zYWN0aW9ucyIsImFtciI6WyJwd2QiXX0.IoWJw_J2xO6vV3SqlaLM9cPiAPYPXqYiEfoqImSZlpNP5Xnge8NTbMbGg5z6xz0lYo6XW8zv-loat8Swa9TnlRoHUKvFell782jJ4mVG9AC8hZs919cwXgSJZAAqla9zwUlmNEoN_sXsKNQA_J_C6X-WBwLmDZzVLlUv_QrHRrOnXMs3c26BHzsaDI-ny55krWWxMnWwn3kM9IJj1mFZuToECt2BXa77G_IX1g5RS9OukhQYBVgl_tuKXHX9p0hZ7B74SsdaTyugORq5EnzjoZU1r8rY9w-PSaX9K_dzrKDmZSLd43tSLmWPknDa26lzZB7vrD4kUYMDBQaG0NSw0g'
#         serializer = XeroEmployeeSerializer(data=request.data)
#
#         headers = {
#             'Authorization': f'Bearer {XERO_API_TOKEN}',
#             'xero-tenant-id': '45d3352a-1557-4787-b0a1-d2827a8dd9fc',
#             'Content-Type': 'application/json',
#             'Accept': 'application/json',
#         }
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         employee_data = serializer.data
#         response = requests.post(XERO_API_URL, json={"Employees": employee_data}, headers=headers)
#         breakpoint()
#         if response.status_code in [200, 201]:
#             return Response(response.json(), status=response.status_code)
#         else:
#             return Response(response.json(), status=response.status_code)
