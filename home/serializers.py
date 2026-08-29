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

        # Your existing validation code...
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

        appointment_day = appointment_date.strftime("%A")

        working_days = [
            day.strip()
            for day in doctor.working_days.split(",")
        ]

        if appointment_day not in working_days:
            raise serializers.ValidationError(
                f"Doctor is not available on {appointment_day}."
            )

        if not doctor.available_from <= time_slot <= doctor.available_until:
            raise serializers.ValidationError(
                f"Doctor is available only between "
                f"{doctor.available_from} and {doctor.available_until}."
            )

        queryset = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            time_slot=time_slot
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "This doctor is already booked for this date and time."
            )

        return data

    # 👇 ADD THIS HERE
    def validate_status(self, value):

        if self.instance:
            current_status = self.instance.status

            if current_status == "completed" and value == "cancelled":
                raise serializers.ValidationError(
                    "A completed appointment cannot be cancelled."
                )

        return value

class AIRecommendationSerializer(serializers.Serializer):

    symptom = serializers.CharField(
        required=True,
        allow_blank=False
    )

    body_area = serializers.CharField(
        required=True,
        allow_blank=False
    )