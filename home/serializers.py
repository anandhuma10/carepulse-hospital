from rest_framework import serializers
from .models import Department, Doctor,Appointment 


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("patient", "created_at")

    def validate(self, data):

        doctor = data.get("doctor")
        appointment_date = data.get("appointment_date")
        time_slot = data.get("time_slot")

        queryset = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=time_slot
        )

        # If updating an existing appointment,
        # exclude the appointment being updated.
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "This doctor is already booked for this date and time."
            )

        return data