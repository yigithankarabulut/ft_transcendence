from django.db import models
from django.utils import timezone

class Friends(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    sender_id = models.PositiveIntegerField(null=False, default=0, help_text="Sender ID")
    receiver_id = models.PositiveIntegerField(null=False, default=0, help_text="Receiver ID")
    state = models.PositiveIntegerField(default=0, help_text="0: Pending, 1: Accepted, 2: Rejected, 3: Blocked")

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.save()
