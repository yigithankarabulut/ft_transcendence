from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
import requests
from apigateway.apigateway.settings import SERVICE_ROUTES

class APIGatewayViewSet(viewsets.ViewSet):
    def dispatch(self, request, *args, **kwargs):
        headers = {'user_id': request.user_id}
        return self.pass_request_to_destination_service(request, headers)

    def pass_request_to_destination_service(self, request, headers):
        base_url = self.get_service_url(request.path)
        if not base_url:
            return Response({'error': 'Invalid path'}, status=status.HTTP_404_NOT_FOUND)

        destination_service_url = f"{base_url}{request.path}"
        method = request.method.lower()
        data = request.data

        response = getattr(requests, method)(destination_service_url, data=data, headers=headers)
        if response.status_code != 200:
            return Response({'error': 'Destination service error'}, status=response.status_code)

        return Response(response.json(), status=response.status_code)

    def get_service_url(self, path):
        for route, url in SERVICE_ROUTES.items():
            if path.startswith(route):
                return url
        return None
