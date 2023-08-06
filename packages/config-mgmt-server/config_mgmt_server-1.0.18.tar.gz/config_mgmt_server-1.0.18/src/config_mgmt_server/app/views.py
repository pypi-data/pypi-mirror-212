from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ISOFile
from .serializers import ISOFileSerializer
 
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/items',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }
 
    return Response(api_urls)

@api_view(['GET'])
def ListISOs(request):
    
    return Response({})
@api_view(['POST'])
def ISOCreate(request):
    return Response({})
@api_view(['POST'])
def UpdateISO(request, pk):
    return Response({})
@api_view(['DELETE'])
def ISODelete(request, pk):
    return Response('item successfully deleted')