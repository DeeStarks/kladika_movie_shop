from django.urls import path
from rental import views

app_name = "rental"

urlpatterns = [
    path('max-rents', views.MaxRentView.as_view(), name='max_rent'),
    path('admin/max-rents', views.MaxRentView.as_view(), name='admin__max_rent'),
    path('user/movies', views.Movie.as_view(), name='user_movies'),
    path('user/movies/rent', views.MovieRental.as_view(), name='rent_movie'),
    path('user/movies/return', views.MovieReturn.as_view(), name='return_movie'),
]