from core.models.expert import Expert
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.retrievers.expert import *
from core.senders.expert import *
from core.utils.general import *

class ExpertViewset(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self,request):
        context = get_experts()
        return Response(context,status=status.HTTP_200_OK)

    def retrieve(self, request, id):
        """
        Retrieve an expert object
        """
        expert = get_expert_by_id(id)
        if not expert:
            context = {
                "error": "Expert does not exist"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        context = {
            "detail": "Expert retrieved successfully",
            "expert": get_expert_information(expert)
        }  
        return Response(context, status=status.HTTP_200_OK)
        
    
    def create(self, request)->Response:
        """Create expert

        Args:
            request (http): http request

        Returns:
            http Response: http response
        """
        user = get_user_from_jwttoken(request)
        if user.expert:
            context = {
                "error": "Expert already exists"
            }
            return Response(context, status=status.HTTP_208_ALREADY_REPORTED)
        expert = create_expert(request.data)
        
        user.expert = get_expert_by_id(expert['expert_id'])
        user.save()
        context = {
            "detail": "Expert created successfully",
            "expert": expert
        }
        
        return Response(context, status=status.HTTP_201_CREATED)  
        
        
    def update(self, request)->Response:
        """Update expert

        Args:
            request (http): http request

        Returns:
            Response: http response
        """
        user = get_user_from_jwttoken(request)
        if not user.expert:
            context = {
                "error": "Expert does not exist"
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
        expert = update_expert(request.data, user.expert)
        if not expert:
            context = {
                "error": "Expert update failed"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        context = { 
            "detail": "Expert updated successfully",
            "expert": expert
        }
        return Response(context, status=status.HTTP_200_OK)