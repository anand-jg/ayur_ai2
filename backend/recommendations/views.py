from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Count
from .models import DoctorReview, Appointment, DoctorRecommendation
from .serializers import (
    DoctorReviewSerializer, AppointmentSerializer,
    DoctorRecommendationSerializer, DoctorSearchSerializer,
    AppointmentRequestSerializer
)
from users.models import DoctorProfile
from ai.models import AIPrompt, AIResponse

class DoctorReviewViewSet(viewsets.ModelViewSet):
    queryset = DoctorReview.objects.all()
    serializer_class = DoctorReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DoctorReview.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'])
    def book(self, request):
        serializer = AppointmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            doctor = DoctorProfile.objects.get(id=serializer.validated_data['doctor_id'])
            appointment = Appointment.objects.create(
                user=request.user,
                doctor=doctor,
                date=serializer.validated_data['date'],
                time=serializer.validated_data['time'],
                notes=serializer.validated_data.get('notes', '')
            )
            return Response(AppointmentSerializer(appointment).data,
                          status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorRecommendation.objects.all()
    serializer_class = DoctorRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DoctorRecommendation.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def search(self, request):
        serializer = DoctorSearchSerializer(data=request.query_params)
        if serializer.is_valid():
            queryset = DoctorProfile.objects.all()
            
            if serializer.validated_data.get('specialization'):
                queryset = queryset.filter(
                    specialization__icontains=serializer.validated_data['specialization']
                )
            
            if serializer.validated_data.get('location'):
                queryset = queryset.filter(
                    user__address__icontains=serializer.validated_data['location']
                )
            
            if serializer.validated_data.get('min_rating'):
                queryset = queryset.filter(
                    rating__gte=serializer.validated_data['min_rating']
                )
            
            if serializer.validated_data.get('max_fee'):
                queryset = queryset.filter(
                    consultation_fee__lte=serializer.validated_data['max_fee']
                )
            
            # Get recommendation prompt template
            prompt_template = AIPrompt.objects.filter(type='recommendation').first()
            if prompt_template:
                # Prepare data for AI
                user_data = {
                    'health_profile': request.user.health_profile.__dict__ if hasattr(request.user, 'health_profile') else {},
                    'previous_appointments': list(Appointment.objects.filter(
                        user=request.user
                    ).values()),
                    'previous_reviews': list(DoctorReview.objects.filter(
                        user=request.user
                    ).values())
                }
                
                # Create AI response
                ai_response = AIResponse.objects.create(
                    prompt=prompt_template,
                    user=request.user,
                    input_data={
                        'user_data': user_data,
                        'doctor_list': list(queryset.values())
                    },
                    response='',  # This would be filled by the AI service
                    metadata={'search_params': serializer.validated_data}
                )
            
            return Response(DoctorProfileSerializer(queryset, many=True).data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
