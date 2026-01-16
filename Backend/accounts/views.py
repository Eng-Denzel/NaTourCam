from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer, AdminUserUpdateSerializer


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if email and password:
        user = authenticate(request, email=email, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({
            'error': 'Email and password are required'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        request.user.auth_token.delete()
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)
    except:
        return Response({
            'error': 'Error logging out'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def admin_update_user(request, user_id):
    """
    Admin endpoint to update user status and permissions
    Only accessible by superusers
    """
    if not request.user.is_superuser:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({
            'error': 'User not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Prevent admin from modifying their own superuser status
    if user.id == request.user.id and 'is_superuser' in request.data:
        return Response({
            'error': 'You cannot modify your own superuser status'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = AdminUserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'User updated successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
