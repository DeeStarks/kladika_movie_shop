from django.shortcuts import render
from rest_framework import views, authentication, permissions, status
from rest_framework.response import Response
from rental import serializers
from rental.models import RentMovie, MaxRent
from datetime import datetime

# Create your views here.
class Movie(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        serializer = serializers.RentalSerializer(
            RentMovie.objects.select_related('movie', 'user').filter(user=request.user),
            context={'request': request},
            many=True
        )
        return Response(data={
            'data' : serializer.data,
            'message': 'Movies retrieved successfully.'
        })

class MovieRental(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        # First make sure "movie" field is passed
        movie_id = request.data.get("movie")
        if not movie_id:
            return Response(data={
                'data': {
                    "movie": ["movie field is required"]
                },
                'message': 'Rent failed.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        request.data['user'] = request.user.id
        # Check if the user has exceeded the maximum number of rentals
        max_rent = MaxRent.objects.get(id=1)
        if RentMovie.objects.select_related('movie', 'user').filter(user=request.user, returned_at=None).count() >= max_rent.number:
            return Response(data={
                'data': {},
                'message': 'You have exceeded the maximum number of movies you can rent.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if user has already rented the movie
        if RentMovie.objects.select_related('movie', 'user').filter(user=request.user, movie=request.data['movie'], returned_at=None).exists():
            return Response(data={
                'data': {},
                'message': 'You have already rented this movie.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        # Proceed to rent the movie
        serializer = serializers.RentalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'data': serializer.data,
                'message': 'Movie was successfully rented.'
            }, status=status.HTTP_201_CREATED)
        return Response(data={
            'data': serializer.errors,
            'message': 'Rental creation failed.',
            'error': True
        }, status=status.HTTP_400_BAD_REQUEST)

class MovieReturn(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        # First make sure "movie" field is passed
        movie_id = request.data.get("movie")
        if not movie_id:
            return Response(data={
                'data': {
                    "movie": ["movie field is required"]
                },
                'message': 'Rent failed.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        movie = RentMovie.objects.select_related("user", "movie").filter(user=request.user, movie=request.data['movie'])
        if movie.exists():
            movie = movie[0]
        else:
            movie = None

        # Check if movie is empty, hence movie is either not rented or already returned
        if not movie:
            return Response(data={
                'data': {},
                'message': 'You have not rented this movie or it has already been returned.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the returned_at field
        movie.returned_at = datetime.now()
        movie.save()

        return Response(data={
            'data': serializers.RentalSerializer(movie).data,
            'message': 'Movie was successfully returned.'
        })

class MaxRentView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get_permissions(self):
        if self.request.method == 'PUT':
            # Only an admin can update maximum rent number
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return [permissions.AllowAny()]

    def get(self, request):
        max_rent = MaxRent.objects.get_or_create(id=1)[0]
        serializer = serializers.MaxRentSerializer(max_rent)
        return Response(data={
            'data' : serializer.data,
            'message': 'Max rent retrieved successfully.'
        })

    def put(self, request):
        max_rent = MaxRent.objects.get_or_create(id=1)[0]
        new_max = request.data.get("number")

        if not new_max:
            return Response(data={
                'data': {
                    "number": ["number is required"]
                },
                'message': 'Max rent update failed.',
                'error': True
            }, status=status.HTTP_400_BAD_REQUEST)

        max_rent.number = new_max
        max_rent.save()
        serializer = serializers.MaxRentSerializer(max_rent)
        return Response(data={
            'data': serializer.data,
            'message': 'Max rent updated successfully.'
        }, status=status.HTTP_200_OK)
