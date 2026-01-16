from rest_framework import generics, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
# Remove GeoDjango imports for now
from django_filters.rest_framework import DjangoFilterBackend
from .models import TouristSite, BilingualContent, Region, SiteImage
from .serializers import TouristSiteListSerializer, TouristSiteSerializer, BilingualContentSerializer, RegionSerializer, AdminTouristSiteUpdateSerializer, AdminTouristSiteCreateSerializer, SiteImageSerializer


class TouristSiteListView(generics.ListAPIView):
    queryset = TouristSite.objects.filter(is_active=True)
    serializer_class = TouristSiteListSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['region']
    search_fields = ['name', 'description', 'address']


class TouristSiteDetailView(generics.RetrieveAPIView):
    queryset = TouristSite.objects.filter(is_active=True)
    serializer_class = TouristSiteSerializer
    permission_classes = [AllowAny]


# Remove geospatial functionality for now


class BilingualContentView(generics.ListAPIView):
    queryset = BilingualContent.objects.all()
    serializer_class = BilingualContentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['site', 'language']


class RegionListView(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def admin_update_site(request, site_id):
    """
    Admin endpoint to update tourist site details and status
    Only accessible by superusers
    """
    if not request.user.is_superuser:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        site = TouristSite.objects.get(id=site_id)
    except TouristSite.DoesNotExist:
        return Response({
            'error': 'Tourist site not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AdminTouristSiteUpdateSerializer(site, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Tourist site updated successfully',
            'site': serializer.data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_create_site(request):
    """
    Admin endpoint to create new tourist site
    Only accessible by superusers
    """
    if not request.user.is_superuser:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    serializer = AdminTouristSiteCreateSerializer(data=request.data)
    if serializer.is_valid():
        site = serializer.save()
        return Response({
            'message': 'Tourist site created successfully',
            'site': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_upload_site_image(request, site_id):
    """
    Admin endpoint to upload images for a tourist site
    Only accessible by superusers
    """
    if not request.user.is_superuser:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        site = TouristSite.objects.get(id=site_id)
    except TouristSite.DoesNotExist:
        return Response({
            'error': 'Tourist site not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Get the uploaded file
    image_file = request.FILES.get('image')
    if not image_file:
        return Response({
            'error': 'No image file provided'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Get optional fields
    caption = request.data.get('caption', '')
    is_primary = request.data.get('is_primary', 'false').lower() == 'true'
    
    # If this is set as primary, unset other primary images
    if is_primary:
        SiteImage.objects.filter(site=site, is_primary=True).update(is_primary=False)
    
    # Create the image
    site_image = SiteImage.objects.create(
        site=site,
        image=image_file,
        caption=caption,
        is_primary=is_primary
    )
    
    serializer = SiteImageSerializer(site_image)
    return Response({
        'message': 'Image uploaded successfully',
        'image': serializer.data
    }, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def admin_delete_site_image(request, image_id):
    """
    Admin endpoint to delete a site image
    Only accessible by superusers
    """
    if not request.user.is_superuser:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        image = SiteImage.objects.get(id=image_id)
    except SiteImage.DoesNotExist:
        return Response({
            'error': 'Image not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Delete the image file and database record
    image.image.delete()  # Delete the file from storage
    image.delete()  # Delete the database record
    
    return Response({
        'message': 'Image deleted successfully'
    }, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_set_primary_image(request, image_id):
    """
    Admin endpoint to set an image as primary
    Only accessible by superusers
    """
    if not request.user.is_superuser:
        return Response({
            'error': 'You do not have permission to perform this action'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        image = SiteImage.objects.get(id=image_id)
    except SiteImage.DoesNotExist:
        return Response({
            'error': 'Image not found'
        }, status=status.HTTP_404_NOT_FOUND)
    
    # Unset other primary images for this site
    SiteImage.objects.filter(site=image.site, is_primary=True).update(is_primary=False)
    
    # Set this image as primary
    image.is_primary = True
    image.save()
    
    serializer = SiteImageSerializer(image)
    return Response({
        'message': 'Primary image set successfully',
        'image': serializer.data
    }, status=status.HTTP_200_OK)
