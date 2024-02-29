import requests
from django.http import JsonResponse
from apigateway.apigateway.settings import SERVICE_ROUTES

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.paths_to_exclude = ['/login', '/register', '/forget_password']

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path in self.paths_to_exclude:
            return None

        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Missing token'}, status=401)

        response = requests.post(f"{SERVICE_ROUTES['/auth']}/token/verify", headers={'Authorization': token})
        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        request.user_id = response.json().get('user_id')
        return None