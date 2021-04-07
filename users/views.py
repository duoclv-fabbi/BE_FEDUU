from django.shortcuts import render
from django.contrib.auth.models import User as User_auth
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import CursorPagination, PageNumberPagination

from .serializers import GetAllUserSerializer, ChangePasswordSerializer, UpdateUserSerializer, UploadPhotoSerializer, \
    CreateUserSerializer
from .managers import UserManager
from .models import User as UserModel
from .models import PhotoModel
from utils import exception


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(CustomTokenRefreshSerializer, self).validate(attrs)
        decoded_payload = token_backend.decode(data['access'], verify=True)
        user_uid = decoded_payload['user_id']

        # add filter query
        user = UserModel.objects.filter(id=user_uid).first()
        data['username'] = user.username
        data['email'] = user.email
        data['name'] = user.name
        data['phone'] = user.phone
        data['position'] = user.position
        if hasattr(user.photo, 'id') is True:
            data['photo'] = {
                'id': user.photo.id,
                'name': "image.png",
                'status': "done",
                'path': user.photo.photo.name,
            }
        else:
            data['photo'] = {
                'id': "",
                'name': "image.png",
                'status': "done",
                'path': "",
            }
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses hereimages_user
        print(self.user, self.user.photo, 'user')
        data['id'] = self.user.id
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['name'] = self.user.name
        data['phone'] = self.user.phone
        data['position'] = self.user.position
        if hasattr(self.user.photo, 'id') is True:
            data['photo'] = {
                'id': self.user.photo.id,
                'name': "image.png",
                'status': "done",
                'path': self.user.photo.photo.name,
            }
        else:
            data['photo'] = {
                'id': "",
                'name': "image.png",
                'status': "done",
                'path': "",
            }
        return data

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LoginWithNoPassworsSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...
        return token

    def validate(self, attrs):
        data = {}
        username = attrs.get('username', None)
        user = UserModel.objects.filter(username=username).exclude(account_type=0).first()
        if user is None:
            raise exception.APIException(detail="authen failed!")
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # # Add extra responses here
        print(user, user.photo, 'user')
        data['id'] = user.id
        data['username'] = user.username
        data['email'] = user.email
        data['name'] = user.name
        data["phone"] = user.phone
        data['position'] = user.position

        if hasattr(user.photo, 'id') is True:
            data['photo'] = {
                'id': user.photo.id,
                'name': "image.png",
                'status': "done",
                'path': user.photo.photo.name,
            }
        else:
            data['photo'] = {
                'id': "",
                'name': "image.png",
                'status': "done",
                'path': "",
            }
        return data


class LoginWithNoPasswordView(TokenObtainPairView):
    serializer_class = LoginWithNoPassworsSerializer


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom Refresh token View
    """
    serializer_class = CustomTokenRefreshSerializer


class GetAllUserView(generics.GenericAPIView):
    # queryset = UserModel.objects.all()
    serializer_class = GetAllUserSerializer

    # pagination_class = PageNumberPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title', 'new_price']

    def get(self, request, *args, **kwargs):
        users = UserModel.objects.all()
        photos = PhotoModel.objects.prefetch_related('photo_user').filter(photo_user__id=1)
        print(photos, 'photos')
        # for user in users:
        #     print(user.photo,'photo')
        serializer = GetAllUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CreateUserView(generics.GenericAPIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise exception.APIException()


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User_auth
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise exception.APIException


class ResetPasswordView(generics.UpdateAPIView):
    """
    An endpoint for reset password.
    """
    serializer_class = ChangePasswordSerializer
    model = User_auth
    permission_classes = [IsAuthenticated]

    def get_object(self, request):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        instance = self.get_object(request)
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise exception.APIException


# for admin
class DeleteUserView(generics.DestroyAPIView):
    model = User_auth
    permission_classes = []

    def destroy(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = UserModel.objects.filter(id=pk)
        all_user = UserModel.objects.all()
        if user.count() > 0:
            self.perform_destroy(all_user)
            return Response(data={}, status=status.HTTP_200_OK)
        raise exception.DoesNotExist(detail=f"{pk} do not exited!")


class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer
    model = UserModel
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise exception.APIException


class UploadPhotoView(generics.GenericAPIView):
    serializer_class = UploadPhotoSerializer
    model = PhotoModel
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        raise exception.APIException