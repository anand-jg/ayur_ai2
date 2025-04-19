from rest_framework import serializers
from .models import AIDecisionPoint, AIPrompt, AIResponse, AILog

class AIDecisionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIDecisionPoint
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AIPromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPrompt
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

class AIResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIResponse
        fields = '__all__'
        read_only_fields = ('created_at',)

class AILogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AILog
        fields = '__all__'
        read_only_fields = ('created_at',)

class AIDecisionRequestSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    category = serializers.ChoiceField(choices=AIDecisionPoint.CATEGORY_CHOICES)
    context = serializers.JSONField()

class AIPromptRequestSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=AIPrompt.TYPE_CHOICES)
    variables = serializers.JSONField()

class AIAnalysisRequestSerializer(serializers.Serializer):
    user_responses = serializers.JSONField()
    context = serializers.JSONField(required=False) 