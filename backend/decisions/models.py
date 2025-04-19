from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Question(models.Model):
    CATEGORY_CHOICES = (
        ('general', 'General Health'),
        ('symptoms', 'Symptoms'),
        ('lifestyle', 'Lifestyle'),
        ('diet', 'Diet'),
        ('mental', 'Mental Health'),
    )
    
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_root = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category} - {self.text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    next_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name='previous_answers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.question.text[:30]}... -> {self.text}"

class UserResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question', 'session_id')

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}..."

class Diagnosis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnoses')
    session_id = models.CharField(max_length=100)
    summary = models.TextField()
    recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Diagnosis for {self.user.username} - {self.created_at}"
