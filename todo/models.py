from django.db import models

# Create your models here.

class Todo(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    compeleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    
    
    def __str__(self):
        return self.title
    
