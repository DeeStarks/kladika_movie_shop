from rest_framework import serializers
from rental import models

class RentalSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RentalSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        # Set the depth based on the request:
        # setting depth to 1 will throw an integrity error on POST requests
        # if the value of the related field is just a number
        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 1

    class Meta:
        model = models.RentMovie
        fields = ('id', 'user', 'movie', 'rented_at', 'returned_at')
        extra_kwargs = {
            'user': {'required': True},
            'movie': {'required': True},
        }

class MaxRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaxRent
        fields = ('number',)
        extra_kwargs = {
            'number': {'required': True}
        }