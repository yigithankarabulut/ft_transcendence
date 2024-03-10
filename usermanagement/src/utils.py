from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.utils.timezone import now


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
