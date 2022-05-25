from rest_framework import permissions
from rest_framework import views
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework.authtoken.models import Token
from utils.response import create_template
from utils.renderer import JSONResponseRenderer
from rest_framework import status, authentication
from . import serializers

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        url_name = request.resolver_match.url_name # used to know if request is either from user or admin
        is_staff_request = True if url_name == 'admin_login' else False
        serializer = serializers.LoginSerializer(
            data={
                **self.request.data,
                '_is_staff': is_staff_request
            },
            context={ 'request': self.request }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(data={ 
                'message': str(e),
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        login(request, user)

        # Return a response containing the user's token
        token = Token.objects.get_or_create(user=user)[0]
        return Response(data={
            'data' : {
                **serializers.UserSerializer(user).data,
                'token': token.key
            },
            'message': 'Admin logged in successfully.' if is_staff_request else 'User logged in successfully.',
        })

class UserRegisterView(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(
            data=self.request.data,
            context={ 'request': self.request }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                data={'message': str(e), 'error': True},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.create_user(serializer.validated_data)
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

class AdminRegisterView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        serializer = serializers.RegisterSerializer(
            data=self.request.data,
            context={ 'request': self.request }
        )

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response(
                data={'message': str(e), 'error': True},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.create_admin(serializer.validated_data)
        login(request, user)

        # Return a response containing the user's token
        token = Token.objects.create(user=user)
        return Response(data={
            'data': {
                **serializers.UserSerializer(user).data,
                'token': token.key,
            },
            'message': 'Admin was successfully registered'
        })
