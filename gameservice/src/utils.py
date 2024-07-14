from django.utils.timezone import now
import requests
import random


class BaseResponse:
    def __init__(self, err: bool, msg: str, data, pagination=None, stats=None):
        self.err = err
        self.string = {"error": msg}
        self.data = {"message": msg, "data": data}
        self.pagination = pagination
        self.stats = stats

    def res(self):
        if self.err:
            return self.string, self.err
        response_data = self.data
        if self.pagination:
            response_data['pagination'] = self.pagination
        if self.stats:
            response_data['stats'] = self.stats
        return response_data, self.err

