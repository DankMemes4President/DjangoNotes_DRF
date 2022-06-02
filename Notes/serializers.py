from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validate_data):
        user = User.objects.create(
            username=validate_data['username'],
        )
        user.set_password(validate_data['password'])
        user.save()
        return user
