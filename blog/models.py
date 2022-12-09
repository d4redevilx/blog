from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
import uuid
# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (str(uuid.uuid4()), ext)
    return os.path.join('uploads', filename)


def validate_file_size(value):
    # Validators
    return True


class Post(models.Model):
    title = models.CharField(max_length=250)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=False)
    updated = models.DateTimeField(blank=True, null=True)
    image = models.FileField(upload_to=user_directory_path,
                             blank=True,
                             null=True,
                             default='',
                             validators=[
                                 FileExtensionValidator(
                                     allowed_extensions=['jpg']),
                                 validate_file_size
                             ])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
