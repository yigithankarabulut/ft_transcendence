from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.conf import settings

class APIGatewayView(APIView):

    def operations(self, request, path):
        print(request.headers)
        print("selam")
        headers = dict(request.headers)
        if not (settings.EXCLUDED_ROUTES and request.path in settings.EXCLUDED_ROUTES):
            headers['user_id'] = str(request.user_id)
        return self.pass_request_to_destination_service(request, path, headers)

    def pass_request_to_destination_service(self, request, path, headers):
        base_url = self.get_service_url(request.path)
        if not base_url:
            return Response({'error': 'Invalid path'}, status=status.HTTP_404_NOT_FOUND)
        
        full_url = f"{base_url}/{path}"
        params = request.query_params
        if params:
            full_url += f"?{params.urlencode()}"
        method = request.method.lower()

        response = requests.request(method, full_url, headers=headers, json=request.data)
        return Response(response.json(), status=response.status_code)

    def get_service_url(self, path):
        for route, url in settings.SERVICE_ROUTES.items():
            if path.startswith(route):
                return url
        return None

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

    def options(self, request, path):
        return Response(status=status.HTTP_200_OK)
