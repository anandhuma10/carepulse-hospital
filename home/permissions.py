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