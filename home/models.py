from PIL import Image
from django.db import models

# Helper function to keep models clean
def resize_image(image_path, width=800, height=600):
    img = Image.open(image_path)
    if img.height > height or img.width > width:
        img.thumbnail((width, height))
        img.save(image_path)

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='departments/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_image(self.image.path)

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
            resize_image(self.image.path)
            
class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"
    
class AppointmentBooking(models.Model):
    patient_name = models.CharField(max_length=255)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20, default="")
    appointment_date = models.CharField(max_length=100)
    time_slot = models.CharField(max_length=100)
    department = models.CharField(max_length=255)
    doctor_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - {self.appointment_date}"
