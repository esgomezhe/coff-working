from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests
from requests.exceptions import RequestException

class GoogleLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'No ID token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        except RequestException:
            return Response({'error': 'Error connecting to Google'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        if response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        email = data.get('email')
        if not email:
            return Response({'error': 'No email found in token'}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(username=email, email=email)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'key': token.key, 
            'user': {
                'id': user.id, 
                'username': user.username, 
                'email': user.email
            }
        }, status=status.HTTP_200_OK)