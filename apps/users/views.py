from django.shortcuts import render
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Users
from argon2 import PasswordHasher

ph = PasswordHasher()

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response ({"message":"User Created Successfully"}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else : 
        return Response({'message':"BAD REQUEST"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = Users.objects.filter(email = email).first()
    
    if user is None:
        return Response({'error':'Invalid Email'},status = status.HTTP_400_BAD_REQUEST)
    try:
        ph.verify(user.password, password)
    except Exception as e:
        return Response({'error': 'Invalid Password'}, status=status.HTTP_400_BAD_REQUEST)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh' : str(refresh),
        'access': str(refresh.access_token)
    }, status= status.HTTP_200_OK)


@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.data.get('refresh_token')

    if not refresh_token:
        return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        refresh = RefreshToken(refresh_token)  
        access_token = str(refresh.access_token)  

        return Response({'access': access_token}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def logout(request):
    try :
        auth = request.headers.get('Authorization')

        if not auth or not auth.startswith('Bearer '):
            return Response({'error': "no access token provided"},status = status.HTTP_400_BAD_REQUEST)

        access_token = auth.split(' ')[1]

        jwt_authenticator = JWTAuthentication()
        validated_token = jwt_authenticator.get_validated_token(access_token)
        user = jwt_authenticator.get_user(validated_token)

        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)


        return Response({'message':'Successfully logged out'},status= status.HTTP_200_OK)
    
    except Exception as e :
        return Response({'error':str(e)},status =status.HTTP_400_BAD_REQUEST)
