from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=300)
    body = models.TextField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    priority = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='todos')

    def __str__(self):
        return self.title
    
    # class Meta:
    #     ordering = ['priority']
    #     indexes = [
    #         models.Index(fields=('title',))
    #     ]