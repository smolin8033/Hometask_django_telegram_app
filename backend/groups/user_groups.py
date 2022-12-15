from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

teachers_group: Group = get_object_or_404(Group, name="Teachers")
students_group: Group = get_object_or_404(Group, name="Students")
