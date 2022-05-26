from rest_framework import serializers
from movie import models

class MovieSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(MovieSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        # Set the depth based on the request:
        # setting depth to 1 will throw an integrity error on POST requests
        # if the value of the related field is just a number
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = models.Movie
        fields = ('id', 'title', 'movie_type', 'genre', 'rental_price')
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'required': True},
            'movie_type': {'required': True},
            'genre': {'required': True},
            'rental_price': {'required': True}
        }

class MovieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MovieType
        fields = ('id', 'name')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True}
        }

class TypePropertySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TypePropertySerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = models.TypeProperty
        fields = ('id', 'name', 'movie_type')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True},
            'movie_type': {'required': True}
        }

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {'required': True}
        }