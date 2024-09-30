"""
Serializers for the user API views
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import (
    get_user_model,
    authenticate,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = User
        fields = ['email', 'name', 'password',]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 5,
            }
        }

    def create(self, validated_data):
        """create & return user with encrypted password"""
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update & return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class CreateAuthToken(serializers.Serializer):
    """serializer for user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_style': 'password'},
                                     trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'),
                            username=email, password=password)

        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs['user'] = user
        return attrs
