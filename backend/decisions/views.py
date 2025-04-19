from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
import uuid
from .models import Question, Answer, UserResponse, Diagnosis
from .serializers import (
    QuestionSerializer, UserResponseSerializer, DiagnosisSerializer,
    QuestionTreeSerializer, DiagnosisRequestSerializer
)
from ai.models import AIPrompt, AIResponse

# Create your views here.

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def root(self, request):
        root_question = Question.objects.filter(is_root=True).first()
        if not root_question:
            return Response({'message': 'No root question found'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        session_id = str(uuid.uuid4())
        serializer = QuestionTreeSerializer({
            'current_question': root_question,
            'previous_responses': [],
            'session_id': session_id
        })
        return Response(serializer.data)

class UserResponseViewSet(viewsets.ModelViewSet):
    queryset = UserResponse.objects.all()
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserResponse.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def submit_response(self, request):
        serializer = UserResponseSerializer(data=request.data)
        if serializer.is_valid():
            response = serializer.save(user=request.user)
            
            # Get next question
            next_question = response.answer.next_question
            if not next_question:
                # If no next question, generate diagnosis
                return self._generate_diagnosis(request.user, response.session_id)
            
            # Get previous responses for this session
            previous_responses = UserResponse.objects.filter(
                user=request.user,
                session_id=response.session_id
            ).exclude(id=response.id)
            
            serializer = QuestionTreeSerializer({
                'current_question': next_question,
                'previous_responses': previous_responses,
                'session_id': response.session_id
            })
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _generate_diagnosis(self, user, session_id):
        # Get all responses for this session
        responses = UserResponse.objects.filter(
            user=user,
            session_id=session_id
        )
        
        # Get diagnosis prompt template
        prompt_template = AIPrompt.objects.filter(type='diagnosis').first()
        if not prompt_template:
            return Response({'message': 'Diagnosis prompt template not found'},
                          status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Prepare response data for AI
        response_data = [
            {
                'question': response.question.text,
                'answer': response.answer.text
            }
            for response in responses
        ]
        
        # Create AI response
        ai_response = AIResponse.objects.create(
            prompt=prompt_template,
            user=user,
            input_data={'responses': response_data},
            response='',  # This would be filled by the AI service
            metadata={'session_id': session_id}
        )
        
        # Create diagnosis
        diagnosis = Diagnosis.objects.create(
            user=user,
            session_id=session_id,
            summary='',  # This would be filled by the AI service
            recommendations=''  # This would be filled by the AI service
        )
        
        return Response({
            'message': 'Diagnosis generation started',
            'diagnosis_id': diagnosis.id
        })

class DiagnosisViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnosis.objects.all()
    serializer_class = DiagnosisSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Diagnosis.objects.filter(user=self.request.user)
