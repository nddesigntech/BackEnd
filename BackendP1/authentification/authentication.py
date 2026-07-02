import datetime

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

from .models import BlacklistedToken


class JWTAuthentication(authentication.BaseAuthentication):
    # Authentification personnalisée basée sur un token JWT dans l'en-tête Authorization
    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            token = auth_header[1].decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        # Vérifie et décode le token JWT envoyé dans la requête
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token expiré.')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Token invalide.')

        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=payload.get('user_id'))
        except user_model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Utilisateur introuvable.')

        # Vérifie si le token est blacklisté (logout effectué)
        if BlacklistedToken.objects.filter(token=token).exists():
            raise exceptions.AuthenticationFailed('Token invalide ou déconnecté.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('Utilisateur désactivé.')

        return (user, token)

    @staticmethod
    def generate_jwt(user):
        # Génère un token JWT valide 24 heures
        expires = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        payload = {
            'user_id': user.id,
            'exp': expires,
            'username': user.username,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token
