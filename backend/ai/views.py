from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AIDecisionPoint, AIPrompt, AIResponse, AILog
from .serializers import (
    AIDecisionPointSerializer, AIPromptSerializer,
    AIResponseSerializer, AILogSerializer,
    AIDecisionRequestSerializer, AIPromptRequestSerializer,
    AIAnalysisRequestSerializer
)

# Create your views here.

class AIDecisionPointViewSet(viewsets.ModelViewSet):
    queryset = AIDecisionPoint.objects.all()
    serializer_class = AIDecisionPointSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def request_decision(self, request):
        serializer = AIDecisionRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Create decision point
            decision_point = AIDecisionPoint.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                category=serializer.validated_data['category'],
                options=serializer.validated_data['context']
            )
            
            # Log the decision request
            AILog.objects.create(
                level='info',
                message=f"Decision point created: {decision_point.title}",
                context={'category': decision_point.category}
            )
            
            return Response(AIDecisionPointSerializer(decision_point).data,
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AIPromptViewSet(viewsets.ModelViewSet):
    queryset = AIPrompt.objects.all()
    serializer_class = AIPromptSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def generate_response(self, request):
        serializer = AIPromptRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Get prompt template
            prompt_template = AIPrompt.objects.filter(
                type=serializer.validated_data['type']
            ).first()
            
            if not prompt_template:
                return Response({'message': 'Prompt template not found'},
                              status=status.HTTP_404_NOT_FOUND)
            
            # Create AI response
            ai_response = AIResponse.objects.create(
                prompt=prompt_template,
                user=request.user,
                input_data=serializer.validated_data['variables'],
                response='',  # This would be filled by the AI service
                metadata={'type': serializer.validated_data['type']}
            )
            
            # Log the response generation
            AILog.objects.create(
                level='info',
                message=f"AI response generated for {request.user.username}",
                context={'prompt_type': serializer.validated_data['type']}
            )
            
            return Response(AIResponseSerializer(ai_response).data,
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AIResponseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AIResponse.objects.all()
    serializer_class = AIResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AIResponse.objects.filter(user=self.request.user)

class AILogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AILog.objects.all()
    serializer_class = AILogSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def analyze_responses(self, request):
        serializer = AIAnalysisRequestSerializer(data=request.data)
        if serializer.is_valid():
            # Get analysis prompt template
            prompt_template = AIPrompt.objects.filter(type='analysis').first()
            if not prompt_template:
                return Response({'message': 'Analysis prompt template not found'},
                              status=status.HTTP_404_NOT_FOUND)
            
            # Create AI response for analysis
            ai_response = AIResponse.objects.create(
                prompt=prompt_template,
                user=request.user,
                input_data=serializer.validated_data,
                response='',  # This would be filled by the AI service
                metadata={'analysis_type': 'response_analysis'}
            )
            
            # Log the analysis request
            AILog.objects.create(
                level='info',
                message=f"Response analysis requested by {request.user.username}",
                context={'analysis_type': 'response_analysis'}
            )
            
            return Response(AIResponseSerializer(ai_response).data,
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
