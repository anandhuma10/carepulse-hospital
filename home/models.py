import os
from PIL import Image, ImageOps
from django.db import models
from django.contrib.auth.models import User

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
    user = models.OneToOneField(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name="doctor_profile",
)

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    experience = models.IntegerField()
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    # Doctor availability
    working_days = models.CharField(
        max_length=100,
        default="Monday,Tuesday,Wednesday,Thursday,Friday"
    )
    available_from = models.TimeField(default="09:00")
    available_until = models.TimeField(default="17:00")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image and os.path.exists(self.image.path):
            resize_and_crop_image(
                self.image.path,
                width=400,
                height=400
            )

class PatientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="patient_profile"
    )
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
            
class ContactInquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.name}"
    

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    appointment_date = models.DateField()
    time_slot = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "time_slot"],
                name="unique_doctor_appointment_slot",
            )
        ]

    def __str__(self):
        return f"{self.patient.username} - {self.doctor.name} - {self.appointment_date}"
