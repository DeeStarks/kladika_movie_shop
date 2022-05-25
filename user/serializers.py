from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    """
    username = serializers.CharField(
        label="Username",
        max_length=30,
        min_length=3,
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
            attrs['user'] = user
            return attrs
        msg = '"username" and "password" are required.'
        raise serializers.ValidationError(msg, code='authorization')

class RegisterSerializer(serializers.Serializer):
    """
    This serializer defines three fields for registration:
        * username
        * email
        * password
    """
    username = serializers.CharField(
        label="Username",
        max_length=30,
        min_length=3,
        write_only=True
    )
    email = serializers.EmailField(
        label="Email",
        style={'input_type': 'email'},
        max_length=254,
        min_length=3,
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if username and email and password:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                msg = 'Username already exists.'
                raise serializers.ValidationError(msg, code='authorization')
            return attrs
        msg = '"username", "email" and "password" are required.'
        raise serializers.ValidationError(msg, code='authorization')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )
        user.set_password(validated_data.get('password'))
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    This serializer serializes the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email')