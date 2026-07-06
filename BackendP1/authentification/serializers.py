from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import Utilisateur


class UserSerializer(serializers.ModelSerializer):
    # Sérialiseur pour exposer les informations de l'utilisateur
    class Meta:
        model = Utilisateur
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    # Sérialiseur pour l'inscription des nouveaux utilisateurs
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
        extra_kwargs = {
            'role': {'required': False},
        }

    def create(self, validated_data):
        # Crée l'utilisateur et crypte le mot de passe
        password = validated_data.pop('password')
        user = Utilisateur.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    # Sérialiseur pour la connexion via username ou email
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not username and not email:
            raise serializers.ValidationError('Username or email must be provided.')

        if email:
            try:
                # Recherche l'utilisateur par email si fourni
                user = Utilisateur.objects.get(email=email)
                username = user.username
            except Utilisateur.DoesNotExist:
                raise serializers.ValidationError('Impossible de se connecter avec ces informations.')

        # Vérifie les identifiants
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Impossible de se connecter avec ces informations.')

        attrs['user'] = user
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    # Sérialiseur pour modifier un utilisateur existant
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
