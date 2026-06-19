from PIL import Image, ImageOps
from django.db import models

def resize_and_crop_image(image_path, width=800, height=600):
    """
    Opens an image, crops it symmetrically from the center, 
    and resizes it to match exact target layout dimensions.
    """
    img = Image.open(image_path)
    fixed_img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
    fixed_img.save(image_path, quality=90)

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='departments/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            resize_and_crop_image(self.image.path, width=800, height=600)

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    
    # 🌟 FIXED CRITICAL LINK: Changed to a real ForeignKey table link
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    
    experience = models.IntegerField()
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            # Doctor profile headshots look cleanest in perfectly uniform squares
            resize_and_crop_image(self.image.path, width=400, height=400)
            
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
