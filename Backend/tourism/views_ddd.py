"""
DDD-based views for Tourism - Example of using application services
These views use the application layer instead of direct ORM access
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal
from datetime import time
from shared.domain.base import DomainException
from .application.services import get_tourism_service
from .application.commands import (
    CreateDestinationCommand, UpdateDestinationCommand,
    CreateRegionCommand, UpdateRegionCommand
)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_destinations_ddd(request):
    """
    List all active destinations using DDD application service.
    GET /api/tourism/ddd/destinations/
    """
    try:
        service = get_tourism_service()
        
        # Check if filtering by region
        region_id = request.query_params.get('region')
        if region_id:
            destinations = service.get_destinations_by_region(int(region_id))
        else:
            destinations = service.get_all_destinations()
        
        # Convert DTOs to response format
        data = [
            {
                'id': d.id,
                'name': d.name,
                'description': d.description,
                'region_id': d.region_id,
                'location': {
                    'latitude': d.latitude,
                    'longitude': d.longitude,
                    'address': d.address
                } if d.latitude and d.longitude else None,
                'entrance_fee': {
                    'amount': d.entrance_fee,
                    'currency': d.currency,
                    'is_free': d.is_free
                },
                'visiting_hours': {
                    'opening_time': d.opening_time,
                    'closing_time': d.closing_time,
                    'is_open_24_hours': d.is_open_24_hours
                },
                'is_active': d.is_active,
                'images': d.images
            }
            for d in destinations
        ]
        
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def get_destination_ddd(request, destination_id):
    """
    Get a single destination using DDD application service.
    GET /api/tourism/ddd/destinations/{id}/
    """
    try:
        service = get_tourism_service()
        destination = service.get_destination(destination_id)
        
        if not destination:
            return Response(
                {'error': 'Destination not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        data = {
            'id': destination.id,
            'name': destination.name,
            'description': destination.description,
            'region_id': destination.region_id,
            'location': {
                'latitude': destination.latitude,
                'longitude': destination.longitude,
                'address': destination.address
            } if destination.latitude and destination.longitude else None,
            'entrance_fee': {
                'amount': destination.entrance_fee,
                'currency': destination.currency,
                'is_free': destination.is_free
            },
            'visiting_hours': {
                'opening_time': destination.opening_time,
                'closing_time': destination.closing_time,
                'is_open_24_hours': destination.is_open_24_hours
            },
            'is_active': destination.is_active,
            'images': destination.images
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_destination_ddd(request):
    """
    Create a new destination using DDD application service.
    POST /api/tourism/ddd/destinations/
    
    Only accessible by superusers.
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        # Parse request data
        data = request.data
        
        # Parse opening/closing times if provided
        opening_time = None
        closing_time = None
        if data.get('opening_time'):
            opening_time = time.fromisoformat(data['opening_time'])
        if data.get('closing_time'):
            closing_time = time.fromisoformat(data['closing_time'])
        
        # Create command
        command = CreateDestinationCommand(
            name=data['name'],
            description=data['description'],
            region_id=int(data['region_id']),
            latitude=Decimal(str(data['latitude'])) if data.get('latitude') else None,
            longitude=Decimal(str(data['longitude'])) if data.get('longitude') else None,
            address=data.get('address'),
            entrance_fee=Decimal(str(data['entrance_fee'])) if data.get('entrance_fee') else None,
            opening_time=opening_time,
            closing_time=closing_time
        )
        
        # Execute command
        service = get_tourism_service()
        destination_id = service.create_destination(command)
        
        return Response(
            {
                'message': 'Destination created successfully',
                'destination_id': destination_id
            },
            status=status.HTTP_201_CREATED
        )
    
    except DomainException as e:
        return Response(
            {'error': e.message},
            status=status.HTTP_400_BAD_REQUEST
        )
    except KeyError as e:
        return Response(
            {'error': f'Missing required field: {str(e)}'},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['PATCH', 'PUT'])
@permission_classes([IsAuthenticated])
def update_destination_ddd(request, destination_id):
    """
    Update a destination using DDD application service.
    PATCH/PUT /api/tourism/ddd/destinations/{id}/
    
    Only accessible by superusers.
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        data = request.data
        
        # Parse opening/closing times if provided
        opening_time = None
        closing_time = None
        if 'opening_time' in data and data['opening_time']:
            opening_time = time.fromisoformat(data['opening_time'])
        if 'closing_time' in data and data['closing_time']:
            closing_time = time.fromisoformat(data['closing_time'])
        
        # Create command
        command = UpdateDestinationCommand(
            destination_id=destination_id,
            name=data.get('name'),
            description=data.get('description'),
            latitude=Decimal(str(data['latitude'])) if data.get('latitude') else None,
            longitude=Decimal(str(data['longitude'])) if data.get('longitude') else None,
            address=data.get('address'),
            entrance_fee=Decimal(str(data['entrance_fee'])) if 'entrance_fee' in data else None,
            opening_time=opening_time,
            closing_time=closing_time
        )
        
        # Execute command
        service = get_tourism_service()
        service.update_destination(command)
        
        return Response(
            {'message': 'Destination updated successfully'},
            status=status.HTTP_200_OK
        )
    
    except DomainException as e:
        return Response(
            {'error': e.message},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def activate_destination_ddd(request, destination_id):
    """
    Activate a destination using DDD application service.
    POST /api/tourism/ddd/destinations/{id}/activate/
    
    Only accessible by superusers.
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        service = get_tourism_service()
        service.activate_destination(destination_id)
        
        return Response(
            {'message': 'Destination activated successfully'},
            status=status.HTTP_200_OK
        )
    
    except DomainException as e:
        return Response(
            {'error': e.message},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_destination_ddd(request, destination_id):
    """
    Deactivate a destination using DDD application service.
    POST /api/tourism/ddd/destinations/{id}/deactivate/
    
    Only accessible by superusers.
    """
    if not request.user.is_superuser:
        return Response(
            {'error': 'You do not have permission to perform this action'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        service = get_tourism_service()
        service.deactivate_destination(destination_id)
        
        return Response(
            {'message': 'Destination deactivated successfully'},
            status=status.HTTP_200_OK
        )
    
    except DomainException as e:
        return Response(
            {'error': e.message},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def search_destinations_ddd(request):
    """
    Search destinations using DDD application service.
    GET /api/tourism/ddd/destinations/search/?q=query
    """
    try:
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {'error': 'Search query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        service = get_tourism_service()
        destinations = service.search_destinations(query)
        
        data = [
            {
                'id': d.id,
                'name': d.name,
                'description': d.description,
                'region_id': d.region_id,
                'is_active': d.is_active
            }
            for d in destinations
        ]
        
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def list_regions_ddd(request):
    """
    List all regions using DDD application service.
    GET /api/tourism/ddd/regions/
    """
    try:
        service = get_tourism_service()
        regions = service.get_all_regions()
        
        data = [
            {
                'id': r.id,
                'name': r.name,
                'code': r.code,
                'description': r.description
            }
            for r in regions
        ]
        
        return Response(data, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
