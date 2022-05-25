from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from utils.response import create_template
from kladika_movie_shop.renderer import JSONResponseRenderer
from rest_framework import status
from . import serializers

class LoginView(views.APIView):
    renderer_classes = [JSONResponseRenderer]
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(
            data=self.request.data,
            context={ 'request': self.request }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(data={ 
                'message': str(e),
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        login(request, user)

        # Return a response containing the user's token
        token = Token.objects.get(user=user)
        return Response(data={
            'data' : {
                **serializers.UserSerializer(user).data,
                'token': token.key
            },
            'message': 'Login successfully'
        })

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response(
            data={'message': 'Method not allowed'},
            status=405
        )

class RegisterView(views.APIView):
    renderer_classes = [JSONResponseRenderer]
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(
            data=self.request.data,
            context={ 'request': self.request }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                data={'message': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.create(serializer.validated_data)
        login(request, user)

        # Return a response containing the user's token
        token = Token.objects.create(user=user)
        return Response(data={
            'data': {
                **serializers.UserSerializer(user).data,
                'token': token.key,
            },
            'message': 'User was successfully registered'
        })

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response(
            data={'message': 'Method not allowed'},
            status=405
        )
