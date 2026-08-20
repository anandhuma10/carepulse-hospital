from rest_framework.permissions import BasePermission


class DepartmentPermission(BasePermission):

    def has_permission(self, request, view):

        # Anyone can read departments
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write operations require login
        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            return request.user.has_perm("home.add_department")

        if request.method in ["PUT", "PATCH"]:
            return request.user.has_perm("home.change_department")

        if request.method == "DELETE":
            return request.user.has_perm("home.delete_department")

        return False


class DoctorPermission(BasePermission):

    def has_permission(self, request, view):

        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return request.user.is_authenticated

        if request.user.is_superuser:
            return True

        return request.user.has_perm(f'home.{self.get_permission_codename(request.method)}')

    def get_permission_codename(self, method):

        permissions = {
            'POST': 'add_doctor',
            'PUT': 'change_doctor',
            'PATCH': 'change_doctor',
            'DELETE': 'delete_doctor',
        }

        return permissions.get(method)

class AppointmentPermission(BasePermission):

    def has_permission(self, request, view):

        # User must be logged in for appointments
        if not request.user.is_authenticated:
            return False

        # Admin has full access
        if request.user.is_superuser:
            return True

        # Reception staff can manage appointments
        if request.user.groups.filter(name="Reception").exists():
            return True

        # Patients can create and access their own appointments
        if request.method in ["GET", "POST", "HEAD", "OPTIONS"]:
            return True

        # Patients can modify/delete their own appointment
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return True

        return False