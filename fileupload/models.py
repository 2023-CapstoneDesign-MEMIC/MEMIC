from django.db import models
from django.db import models
class UploadFileModel(models.Model):
    description = models.CharField(max_length=255)
    files = models.FileField(upload_to="documents",null=True)
    upload_at = models.DateTimeField(auto_now=True)
class FileUpload(models.Model):
    title = models.TextField(max_length=40, null=True)
    imgfile = models.FileField(null=True, upload_to="", blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title


