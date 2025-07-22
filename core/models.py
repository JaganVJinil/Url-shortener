from django.db import models
from django.contrib.auth.models import User
import string, random

def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortURL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    original_url = models.URLField()
    short_url = models.CharField(max_length=10, unique=True, default=generate_short_url)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
