from rest_framework import serializers
from .models import Question, Answer, UserResponse, Diagnosis

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'text', 'next_question')

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'category', 'is_root', 'answers')

class UserResponseSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    answer_text = serializers.CharField(source='answer.text', read_only=True)

    class Meta:
        model = UserResponse
        fields = ('id', 'question', 'answer', 'question_text', 'answer_text', 'session_id', 'created_at')
        read_only_fields = ('user', 'session_id', 'created_at')

class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diagnosis
        fields = ('id', 'summary', 'recommendations', 'created_at')
        read_only_fields = ('user', 'session_id', 'created_at')

class QuestionTreeSerializer(serializers.Serializer):
    current_question = QuestionSerializer()
    previous_responses = UserResponseSerializer(many=True)
    session_id = serializers.CharField()

class DiagnosisRequestSerializer(serializers.Serializer):
    session_id = serializers.CharField()
    responses = UserResponseSerializer(many=True) 