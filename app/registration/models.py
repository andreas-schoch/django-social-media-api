from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
VALIDATION_CODE_LENGTH = 16


class CodeStatus:
    pending = 'PENDING'
    validated = 'VALIDATED'


FRIEND_CHOICES = (
    (CodeStatus.pending, 'PENDING'),
    (CodeStatus.validated, 'VALIDATED'),
)


class ValidationCode(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='validator', null=True, blank=True)
    code = models.CharField(max_length=VALIDATION_CODE_LENGTH, null=True, blank=True)
    status = models.CharField(max_length=12, choices=FRIEND_CHOICES, default=CodeStatus.pending)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    # TODO make code only valid for 30min

