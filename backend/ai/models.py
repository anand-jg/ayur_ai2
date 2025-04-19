from django.db import models
from django.contrib.auth import get_user_model
from decisions.models import Question, Answer, UserResponse

User = get_user_model()

class AIDecisionPoint(models.Model):
    CATEGORY_CHOICES = (
        ('ui', 'UI/UX'),
        ('feature', 'Feature Implementation'),
        ('security', 'Security'),
        ('performance', 'Performance'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    options = models.JSONField()  # Stores different approaches with pros and cons
    selected_option = models.CharField(max_length=255, blank=True)
    rationale = models.TextField(blank=True)
    impact = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.title}"

class AIPrompt(models.Model):
    TYPE_CHOICES = (
        ('diagnosis', 'Diagnosis'),
        ('recommendation', 'Doctor Recommendation'),
        ('general', 'General Health'),
    )
    
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    template = models.TextField()
    variables = models.JSONField()  # Stores required variables for the prompt
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.type} Prompt Template"

class AIResponse(models.Model):
    prompt = models.ForeignKey(AIPrompt, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_responses')
    input_data = models.JSONField()  # Stores the input data used for the prompt
    response = models.TextField()
    metadata = models.JSONField(blank=True)  # Stores additional metadata about the response
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI Response for {self.user.username} - {self.created_at}"

class AILog(models.Model):
    LEVEL_CHOICES = (
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    )
    
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    context = models.JSONField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.level} - {self.message[:50]}..."
