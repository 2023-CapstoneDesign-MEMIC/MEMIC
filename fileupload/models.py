from django.db import models
import os
from django.db import models
class FileUpload(models.Model):
    audiofile = models.FileField(upload_to='MEMIC')
    start = models.IntegerField()
    end = models.IntegerField()
    # title = models.TextField(max_length=40, null=True)
    # imgfile = models.FileField(null=True, upload_to="", blank=True)
    # content = models.TextField()

    def __str__(self):
        return self.title


