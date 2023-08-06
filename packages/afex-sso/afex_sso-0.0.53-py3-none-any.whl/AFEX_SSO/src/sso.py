import time
import json
import requests
from django.conf import settings as app_settings

URL = app_settings.SSO_URL


# settings.configure()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SSO.settings")


class SSO:
    """_summary_
    SSO CLASS
    """

    # def __init__(self, sp_api_key, sp_hash_key, session_key) -> None:
    #     self.api = sp_api_key
    #     self.hash = sp_hash_key
    #     self.session = session_key

    # def __call__(self):
    #     return self.check_credentials(self.api, self.hash, self.session)


    def check_credentials(self, sp_api_key, sp_hash_key, session_key):
        try:
            headers = {
                "api-key": sp_api_key,
                "hash-key":  sp_hash_key,
                "request-ts": session_key
            }
            response = requests.get(
                f"{URL}/v1/api/verify_sp/{session_key}", headers=headers)
            data = json.loads(response.text)
            return data

        except Exception as e:
            return f"Something went wrong, please confirm the credentials and try again: {e}"

    def sign_out(self, sp_api_key, sp_hash_key, session_key, email: str):
        try:
            headers = {
                "api-key": sp_api_key,
                "hash-key": sp_hash_key,
                "request-ts": session_key
            }
            data = {
                "email": email
            }
            response = requests.post(
                f"{URL}/v1/api/signout", headers=headers, data=data)
            data = json.loads(response.text)
            return data

        except Exception as e:
            return f"Something went wrong, please confirm the credentials and try again: {e}"

