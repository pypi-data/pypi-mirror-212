
from django.db import models
 
class ISOFile(models.Model):
    name = models.CharField(max_length=255)
    data = models.FileField(upload_to=None)
 
    def __str__(self) -> str:
        return self.name