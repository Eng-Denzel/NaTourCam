from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.signals import user_logged_in
from .models import User, UserProfile, TourOperator
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, TourOperatorSerializer

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            user_logged_in.send(sender=user.__class__, request=request, user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Invalid credentials'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except:
            pass
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class TourOperatorView(generics.RetrieveUpdateAPIView):
    serializer_class = TourOperatorSerializer
    
    def get_object(self):
        try:
            return self.request.user.touroperator
        except TourOperator.DoesNotExist:
            return None

class TourOperatorCreateView(generics.CreateAPIView):
    queryset = TourOperator.objects.all()
    serializer_class = TourOperatorSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CheckAuthView(APIView):
    def get(self, request):
        return Response({
            'is_authenticated': True,
            'user': UserSerializer(request.user).data
        })
