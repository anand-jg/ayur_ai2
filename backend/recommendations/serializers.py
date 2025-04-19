from rest_framework import serializers
from .models import DoctorReview, Appointment, DoctorRecommendation
from users.serializers import DoctorProfileSerializer

class DoctorReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = DoctorReview
        fields = ('id', 'user', 'user_name', 'doctor', 'rating', 'comment', 'created_at')
        read_only_fields = ('user', 'created_at')

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_details = DoctorProfileSerializer(source='doctor', read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'user', 'user_name', 'doctor', 'doctor_details', 
                 'date', 'time', 'status', 'notes', 'created_at')
        read_only_fields = ('user', 'created_at')

class DoctorRecommendationSerializer(serializers.ModelSerializer):
    doctor_details = DoctorProfileSerializer(source='doctor', read_only=True)

    class Meta:
        model = DoctorRecommendation
        fields = ('id', 'doctor', 'doctor_details', 'score', 'reason', 'created_at')
        read_only_fields = ('user', 'created_at')

class DoctorSearchSerializer(serializers.Serializer):
    specialization = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    min_rating = serializers.DecimalField(max_digits=3, decimal_places=2, required=False)
    max_fee = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)

class AppointmentRequestSerializer(serializers.Serializer):
    doctor_id = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()
    notes = serializers.CharField(required=False, allow_blank=True) 