from django.shortcuts import render
from rest_framework import views, authentication, permissions, status
from rest_framework.response import Response
from movie.serializers import MovieSerializer, GenreSerializer, MovieTypeSerializer, TypePropertySerializer
from movie.models import Movie, Genre, MovieType, TypeProperty

# Create your views here.
class MovieList(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]

    # Using different permissions for GET and POST requests
    def get_permissions(self):
        if self.request.method == 'POST':
            # Only an admin can create a movie
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        serializer = MovieSerializer(
            Movie.objects.select_related('genre', 'movie_type').all(), 
            context={'request': request},
            many=True)
        return Response(data={
            'data' : serializer.data,
            'message': 'Movies retrieved successfully.'
        })

    def post(self, request):
        serializer = MovieSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'data': serializer.data,
                'message': 'Movie created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            'data': serializer.errors,
            'message': 'Movie creation failed.',
            'error': True
        }, status=status.HTTP_400_BAD_REQUEST)

class Genres(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only an admin can create a genre
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        serializer = GenreSerializer(Genre.objects.all(), many=True)
        return Response(data={
            'data' : serializer.data,
            'message': 'Genres retrieved successfully.'
        })

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'data': serializer.data,
                'message': 'Genre created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            'data': serializer.errors,
            'message': 'Genre creation failed.',
            'error': True
        }, status=status.HTTP_400_BAD_REQUEST)

class MovieTypes(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only an admin can create a movie type
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        serializer = MovieTypeSerializer(MovieType.objects.all(), many=True)
        return Response(data={
            'data' : serializer.data,
            'message': 'Movie types retrieved successfully.'
        })

    def post(self, request):
        serializer = MovieTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'data': serializer.data,
                'message': 'Movie type created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            'data': serializer.errors,
            'message': 'Movie type creation failed.',
            'error': True
        }, status=status.HTTP_400_BAD_REQUEST)

class MovieTypeProperties(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'POST':
            # Only an admin can create a movie type property
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request, type_id):
        if not type_id:
            return Response(data={
                'data': None,
                'message': 'The type_id parameter is required.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = TypePropertySerializer(
            TypeProperty.objects.select_related("movie_type").filter(movie_type=type_id), 
            context={'request': request},
            many=True
        )
        return Response(data={
            'data' : serializer.data,
            'message': 'Properties retrieved successfully.'
        })

    def post(self, request, type_id):
        if type_id is None:
            return Response(data={
                'data': None,
                'message': 'The type_id parameter is required.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data['movie_type'] = type_id # Add the type_id to the request data

        serializer = TypePropertySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'data': serializer.data,
                'message': 'Movie type property created successfully.'
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            'data': serializer.errors,
            'message': 'Movie type property creation failed.',
            'error': True
        }, status=status.HTTP_400_BAD_REQUEST)