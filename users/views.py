from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from allauth.socialaccount.providers.google import views as google_views
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import requests
from django.conf import settings

class GoogleLogin(APIView):
    def post(self, request):
        token = request.data.get('access_token')
        if not token:
            return Response({'error': 'No access token provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar el token con Google
        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        if response.status_code != 200:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        email = data.get('email')
        if not email:
            return Response({'error': 'No email found in token'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(username=email, email=email)
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({'key': token.key, 'user': {'id': user.id, 'username': user.username, 'email': user.email}}, status=status.HTTP_200_OK)