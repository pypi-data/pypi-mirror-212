from django.db import models

class CaseInsensitiveEmailField(models.EmailField):
    """
    """

    def to_python(self, value):
        """
        """

        value  = super(CaseInsensitiveEmailField, self).to_python(value)
        return value.lower() if isinstance(value, str) else value