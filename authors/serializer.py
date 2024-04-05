from collections import defaultdict

from django.contrib.auth import get_user_model
from rest_framework import serializers

from utils.django_forms import strong_password


class AuthorSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # criar um dicionario dinamico para armazenar os errors de uma vez
        self.__my_errors = defaultdict(list)

    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'

        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    password2 = serializers.CharField(write_only=True)

    password = serializers.CharField(
        write_only=True, validators=[strong_password])

    def validate(self, attrs):

        super_validate = super().validate(attrs)
        cleaned_data = attrs

        if self.instance is None:

            password = cleaned_data.get('password', "")
            password2 = self.initial_data.pop('password2')

            if password2 is None:
                self.__my_errors['password2'].append(
                    'Password must not be empty')

            if password != password2:
                msg = 'passaword and password2 must be equal.'
                self.__my_errors['password'].append(msg)
                self.__my_errors['password2'].append(msg)

        email = cleaned_data.get('email', '')
        email_already_exists = get_user_model().objects.filter(email=email).exists()

        if self.instance is None:
            if email_already_exists:
                self.__my_errors['email'].append(
                    'User e-mail is already in use')
        elif email and self.instance.email != email:
            if email_already_exists:
                self.__my_errors['email'].append(
                    'User e-mail is already in use')

        # Se houver erros, lança uma exceção de validação
        if self.__my_errors:
            raise serializers.ValidationError(self.__my_errors)

        return super_validate

    def create(self, validated_data):
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")

        user = get_user_model().objects.create(**validated_data)
        user.set_password(password)
        user.save()

        return user
