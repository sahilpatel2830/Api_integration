from xero_python.api_client import ApiClient, Configuration
from xero_python.api_client.oauth2 import OAuth2Token
from decouple import config
from xero_python.payrollau import PayrollAuApi


def get_xero_client():
    config_cred= Configuration(
        oauth2_token=OAuth2Token(
            client_id= config("XERO_CLIENT_ID"),
            client_secret=config("XERO_CLIENT_SECRET"),
            redirect_uri = config("XERO_REDIRECT_URI")
        )
    )

    api_client = ApiClient(config_cred)
    return PayrollAuApi(api_client)