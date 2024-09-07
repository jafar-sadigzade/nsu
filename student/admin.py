from django.contrib import admin

from student.models import Student, StudentExamResult


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentExamResult)
class StudentExamResultAdmin(admin.ModelAdmin):
    pass
