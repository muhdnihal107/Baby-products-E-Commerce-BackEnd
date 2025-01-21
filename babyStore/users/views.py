from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email = email).first()
        
        if user is None:
            raise AuthenticationFailed('user not found')
        
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')
        return Response({
            'message':"loginn success",
            'access_token': str(access_token),
            'refresh_token': str(refresh),
            'user':{
                'name': user.name,
                'email':user.email,
                'is_staff': user.is_staff,
            }
        })
        
class LogoutView(APIView):

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response(
                    {'error': 'Refresh token is required for logout'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class ListUsersView(APIView):
    def get(self,request):
        users = User.objects.filter(is_staff=False)
        serializer = UserSerializer(users,many=True)
        if serializer.is_valid:
            return Response(serializer.data)
        return Response(serializer.errors)

            

class UserDetailView(APIView):
    def get(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        