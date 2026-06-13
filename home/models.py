from PIL import Image

from django.db import models

# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='departments/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 800:
                img.thumbnail((800, 600))
                img.save(self.image.path)

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 600 or img.width > 800:
                img.thumbnail((800, 600))
                img.save(self.image.path)
