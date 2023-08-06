from django.db import models

class Base(models.Model):
    """
    """

    MAX_LENGTH_SMALL = 127
    MAX_LENGTH_MEDIUM = 255
    MAX_LENGTH_LARGE = 511

    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        abstract = True
