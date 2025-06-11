from django.db import models
from django.contrib.auth.models import User

class UserMessage(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="out_messages")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="in_messages")
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return "from user: " + self.from_user.username + " " + self.message