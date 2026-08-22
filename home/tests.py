from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Department, Doctor


class AppointmentAPITestCase(APITestCase):

    def setUp(self):
        # Create test patient
        self.user = User.objects.create_user(
            username="testpatient",
            password="testpass123"
        )

        # Create test department
        self.department = Department.objects.create(
            name="Cardiology",
            description="Heart and cardiovascular care"
        )

        # Create test doctor
        self.doctor = Doctor.objects.create(
            name="Dr. Test",
            department=self.department,
            experience=5,
            working_days="Monday,Tuesday,Wednesday,Thursday,Friday",
            available_from="09:00",
            available_until="17:00"
        )

        # Authenticate the test patient
        self.client.force_authenticate(user=self.user)

    def test_create_appointment(self):
        url = reverse("appointment-list")

        data = {
            "appointment_date": "2026-08-24",
            "time_slot": "11:00:00",
            "doctor": self.doctor.id,
            "department": self.department.id
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
    def test_prevent_double_booking(self):
        url = reverse("appointment-list")

        data = {
            "appointment_date": "2026-08-24",
            "time_slot": "11:00:00",
            "doctor": self.doctor.id,
            "department": self.department.id
        }

        # First appointment should succeed
        first_response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            first_response.status_code,
            status.HTTP_201_CREATED
        )

        # Second appointment uses the exact same doctor,
        # date and time
        second_response = self.client.post(
            url,
            data,
            format="json"
        )

        # It should be rejected
        self.assertEqual(
            second_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    def test_reject_appointment_outside_working_hours(self):
        url = reverse("appointment-list")

        data = {
            "appointment_date": "2026-08-24",
            "time_slot": "08:00:00",
            "doctor": self.doctor.id,
            "department": self.department.id
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    def test_reject_appointment_on_non_working_day(self):
        url = reverse("appointment-list")

        data = {
            "appointment_date": "2026-08-23",  # Sunday
            "time_slot": "11:00:00",
            "doctor": self.doctor.id,
            "department": self.department.id
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
    def test_completed_appointment_cannot_be_cancelled(self):
        url = reverse("appointment-list")

        data = {
            "appointment_date": "2026-08-24",
            "time_slot": "11:00:00",
            "doctor": self.doctor.id,
            "department": self.department.id
        }

        # Create appointment
        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        appointment_id = response.data["id"]

        # Mark appointment as completed
        response = self.client.patch(
            f"{url}{appointment_id}/",
            {"status": "completed"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        # Try to cancel completed appointment
        response = self.client.patch(
            f"{url}{appointment_id}/",
            {"status": "cancelled"},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )