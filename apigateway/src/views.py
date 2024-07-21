import logging
import requests
from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class APIGatewayView(APIView):

    def operations(self, request, path):
        headers = dict(request.headers)
        if request.path.startswith('/user/email_verify') or request.path.startswith('/user/reset-password') or request.path.startswith('/user/pwd/change'):
            return pass_request_to_destination_service(request, path, headers)
        if not (settings.EXCLUDED_ROUTES and request.path in settings.EXCLUDED_ROUTES):
            headers['id'] = str(request.user_id)
        return pass_request_to_destination_service(request, path, headers)

    def get(self, request, path):
        return self.operations(request, path)

    def post(self, request, path):
        return self.operations(request, path)

    def put(self, request, path):
        return self.operations(request, path)

    def patch(self, request, path):
        return self.operations(request, path)

    def delete(self, request, path):
        return self.operations(request, path)


def pass_request_to_destination_service(request, path, headers):
    base_url = get_service_url(request.path)
    if not base_url:
        return Response({'error': 'Invalid path'}, status=status.HTTP_404_NOT_FOUND)

    full_url = f"{base_url}/{path}"
    logging.error("--++++++++ full_url: %s", full_url)
    params = request.query_params
    if params:
        full_url += f"?{params.urlencode()}"
    method = request.method.lower()
    if path.startswith('user/email_verify') or path.startswith('user/reset-password'):
        logging.error("---------------------<>>>>>>>>>>>>>>>>> ")
        response = requests.get(full_url)
        json_response = response.json()
        if 'redirect_url' in json_response:
            return HttpResponseRedirect(json_response['redirect_url'])
    try:
        response = requests.request(method, full_url, headers=headers, json=request.data)
    except requests.exceptions.RequestException as e:
        logging.error(f"Error in request: {e}")
        return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if path.startswith('auth/') and response.status_code == 200 or response.status_code == 207:
        json_response = response.json()
        if 'redirect_url' in json_response:
            return HttpResponseRedirect(json_response['redirect_url'])

    if response.headers.get('content-type') == 'application/json':
        return Response(response.json(), status=response.status_code)
    return Response(response.content, status=response.status_code)


def get_service_url(path):
    for route, url in settings.SERVICE_ROUTES.items():
        if path.startswith(route):
            return url
    return None