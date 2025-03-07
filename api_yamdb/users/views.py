from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.permissions import IsAdminOrSuperUser
from users.serializers import (
    TokenSerializer, UserCreationSerializer,
    UserSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete', 'head', 'options')
    permission_classes = (IsAdminOrSuperUser,)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def get_current_user_info(self, request):
        if request.method == 'GET':
            user = get_object_or_404(
                User,
                username=request.user.username
            )
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSignUp(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(message_data):
        email = EmailMessage(
            subject=message_data['subject'],
            body=message_data['body'],
            from_email='admin@yamdb.ru',
            to=[message_data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = UserCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        data = {
            'subject': 'Код подтверждения',
            'body': f'Ваш код подтверждения: {confirmation_code}',
            'to_email': user.email
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetToken(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Такого пользователя не существует'},
                status=status.HTTP_404_NOT_FOUND
            )
        if default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )
