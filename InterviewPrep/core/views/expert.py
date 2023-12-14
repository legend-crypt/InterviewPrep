from rest_framework import viewsets, status
from rest_framework.response import Response
from core.senders.expert import create_expert
from core.retrievers.expert import *
from core.serializers.expert import ExpertSerializer

class ExpertViewSet(viewsets.ViewSet):
    
    def list(self, request) -> Response:
        """List all experts

        Args:
            request (http): http request

        Returns:
            Response: http response
        """
        experts = Expert.objects.all()
        serializer = ExpertSerializer(experts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None) -> Response:
        """Retrieve expert by id

        Args:
            request (http): http request
            pk (uuid): uuid field

        Returns:
            Response: http response
        """
        expert = get_expert_by_id(pk)
        if expert:
            serializer = ExpertSerializer(expert)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Expert not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    def create(self, request) -> Response:
        """Create Expert

        Args:
            request (http): http request

        Returns:
            Response: http response
        """
        email = request.data.get('email')
        expert = get_expert_by_email(email)
        if expert:
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if expert.verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_208_ALREADY_REPORTED)
        
        data = request.data
        expert = create_expert(data)
        if expert:
            return Response(expert, status=status.HTTP_201_CREATED)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    def update(request, pk=None) -> Response:
        """Update Expert

        Args:
            request (http): http request
            pk (uuid): uuid field

        Returns:
            Response: http response
        """
        expert = get_expert_by_id(pk)
        if not expert:
            return Response({'message': 'Expert not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data
        expert = update_expert(expert, data)
        if expert:
            return Response(get_expert_information(expert), status=status.HTTP_200_OK)
        return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)