from django.contrib.auth.tokens import PasswordResetTokenGenerator

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


class ResetPasswordTokenGenerator(PasswordResetTokenGenerator):
    def make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + user.password +
            str(timestamp)
        )
