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

    # For POST, get values from incoming data.
    # For PATCH, use the existing appointment value if not provided.
        doctor = data.get(
            "doctor",
            self.instance.doctor if self.instance else None
        )
        appointment_date = data.get(
            "appointment_date",
            self.instance.appointment_date if self.instance else None
        )
        time_slot = data.get(
            "time_slot",
            self.instance.time_slot if self.instance else None
        )

        # Convert the appointment date into a day name.
        appointment_day = appointment_date.strftime("%A")

        # Convert "Monday,Tuesday,Wednesday" into a Python list.
        working_days = [
            day.strip()
            for day in doctor.working_days.split(",")
        ]

        # Check whether the doctor works on that day.
        if appointment_day not in working_days:
            raise serializers.ValidationError(
                f"Doctor is not available on {appointment_day}."
            )

        # Check whether the selected time is within working hours.
        if not doctor.available_from <= time_slot <= doctor.available_until:
            raise serializers.ValidationError(
                f"Doctor is available only between "
                f"{doctor.available_from} and {doctor.available_until}."
            )

        # Check whether another appointment already uses this slot.
        queryset = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=time_slot
        )

        # Ignore the current appointment when updating.
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "This doctor is already booked for this date and time."
            )

        return data