from django.urls import path
from movie import views

app_name = "movie"

urlpatterns = [
    path('', views.MovieList.as_view(), name='movie_list'),
    path('genres', views.Genres.as_view(), name='genre_list'),
    path('types', views.MovieTypes.as_view(), name='type_list'),
    path('types/properties/<int:type_id>', views.MovieTypeProperties.as_view(), name='type_properties'),
    path('admin/movies', views.MovieList.as_view(), name='admin__movie_list'),
    path('admin/genres', views.Genres.as_view(), name='admin__genre_list'),
    path('admin/types', views.MovieTypes.as_view(), name='admin__type_list'),
    path('admin/types/properties/<int:type_id>', views.MovieTypeProperties.as_view(), name='admin__type_properties'),
]