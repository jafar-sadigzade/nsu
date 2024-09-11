from django.contrib import admin

from student.models import Student, StudentExamResult


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentExamResult)
class StudentExamResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'exam', 'student_answers_json')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'exam__name')
    list_filter = ('exam',)
