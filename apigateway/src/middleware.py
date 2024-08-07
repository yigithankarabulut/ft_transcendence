import logging

import requests
from django.conf import settings
from django.http import JsonResponse


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.paths_to_exclude = settings.EXCLUDED_ROUTES

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/api'):
            request.path = request.path[4:]
        if request.path in self.paths_to_exclude:
            return None

        if request.path.startswith('/user/email_verify') or request.path.startswith('/user/reset-password') or request.path.startswith('/user/pwd/change'):
            return None

        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Missing token'}, status=401)

        response = requests.post(f"{settings.SERVICE_ROUTES['/auth']}/auth/token/validate", headers={'Authorization': token})

        if response.status_code != 200:
            err_msg = response.json().get('error')
            status = response.status_code
            return JsonResponse({'error': err_msg}, status=status)

        request.user_id = response.json().get('user_id')
        return None