from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.timezone import now
from usermanagement.settings import SERVICE_ROUTES
import requests
import random


class BaseResponse:
    def __init__(self, err: bool, msg: str, data, pagination=None):
        self.err = err
        self.string = {"error": msg}
        self.data = {"message": msg, "data": data}
        self.pagination = pagination

    def res(self):
        if self.err:
            return self.string, self.err
        response_data = self.data
        if self.pagination:
            response_data['pagination'] = self.pagination
        return response_data, self.err


def make_hash_value(user, timestamp):
    return (
            str(user.pk) + "-" + str(timestamp)
    )


def check_token_validity(token):
    decoded_token = force_str(urlsafe_base64_decode(token))
    if not decoded_token:
        return "Invalid token"
    timestamp = decoded_token.split("-")[-1]
    if not timestamp:
        return "Invalid token format"
    if now().timestamp() - float(timestamp) > 21600:  # 6 hours in seconds
        return "Token expired"
    return None


def req_to_auth_service_for_generate_token(user_id) -> str:
    try:
        response = requests.post(f"{SERVICE_ROUTES['/auth']}/auth/token", params={"user_id": user_id})
        if response.status_code != 200:
            raise Exception("error")
        token = response.json().get('token')
    except Exception as e:
        return str(e)
    return token


def generate_2fa_code():
    code = random.randint(100000, 999999)
    db_code = str(code) + "-" + str(now().timestamp())
    return code, db_code
