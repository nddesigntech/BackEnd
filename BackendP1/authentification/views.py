import datetime

import jwt
from django.conf import settings
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .authentication import JWTAuthentication
from .models import BlacklistedToken, CustomUser
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, UserUpdateSerializer


class RegisterView(generics.CreateAPIView):
    # Endpoint pour l'inscription d'un nouvel utilisateur
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = JWTAuthentication.generate_jwt(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'token': token,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    # Endpoint pour la connexion et la génération du token JWT
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = JWTAuthentication.generate_jwt(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'token': token,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveAPIView):
    # Endpoint pour récupérer les informations du profil connecté
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class RefreshView(generics.GenericAPIView):
    # Endpoint pour rafraîchir le token JWT
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = JWTAuthentication.generate_jwt(request.user)
        return Response({'token': token}, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    # Endpoint pour déconnecter l'utilisateur en invalidant le token
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        token = request.auth
        if not token:
            return Response({'detail': 'Token manquant.'}, status=status.HTTP_400_BAD_REQUEST)

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        expires_at = datetime.datetime.fromtimestamp(payload.get('exp'), tz=timezone.utc)
        BlacklistedToken.objects.get_or_create(token=token, defaults={'expires_at': expires_at})
        return Response({'detail': 'Déconnexion effectuée.'}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    # Endpoint pour lister tous les utilisateurs (admin uniquement)
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserUpdateView(generics.UpdateAPIView):
    # Endpoint pour modifier un utilisateur existant (admin uniquement)
    queryset = CustomUser.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'pk'


class UserDeleteView(generics.DestroyAPIView):
    # Endpoint pour supprimer un utilisateur (admin uniquement)
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAdminUser]
    lookup_url_kwarg = 'pk'
