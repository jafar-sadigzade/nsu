import json

from django.contrib import admin

from exam.models import Exam, ExamType, ColumnMapping, QuestionType, Subject
from student.models import Student, StudentExamResult


class ColumnMappingInline(admin.TabularInline):
    model = ColumnMapping
    extra = 3


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    inlines = [ColumnMappingInline]


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type_code', 'order', 'number_of_questions', 'points_per_correct', 'points_per_incorrect')
    search_fields = ('name', 'type_code')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    pass


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.students_answers_txt and obj.correct_answers_txt:
            self.save_to_student_result(obj)

    @staticmethod
    def save_to_student_result(exam):
        student_answers_json = exam.student_answers_json
        if isinstance(student_answers_json, str):
            try:
                student_answers_json = json.loads(student_answers_json)
            except json.JSONDecodeError:
                print("Error decoding JSON data")
                return

        if not isinstance(student_answers_json, list):
            print("Expected list but got:", type(student_answers_json))
            return

        for student_data in student_answers_json:
            if isinstance(student_data, dict):
                student_id = student_data.get("İş nömrəsi")

                if not student_id:
                    continue
                try:
                    student = Student.objects.get(student_id=student_id)

                    answers_json = exam.answers_json
                    if isinstance(answers_json, str):
                        try:
                            answers_json = json.loads(answers_json)
                        except json.JSONDecodeError:
                            print("Error decoding exam details JSON")
                            return

                    _, _ = StudentExamResult.objects.update_or_create(
                        student=student,
                        exam=exam,
                        defaults={
                            'answers_json': answers_json,
                            'student_answers_json': student_data
                        }
                    )
                except Student.DoesNotExist:
                    print(f"Student with ID {student_id} not found.")
            else:
                print("Expected dict but got:", type(student_data))
