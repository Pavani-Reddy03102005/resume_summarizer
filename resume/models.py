from django.db import models
from django.contrib.auth.models import User

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    original_filename = models.CharField(max_length=255)

    candidate_name = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    ai_summary = models.TextField(blank=True)
    job_match_score = models.IntegerField(null=True)

    status = models.CharField(max_length=50, default='pending')


class SkillTag(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.CharField(max_length=100)