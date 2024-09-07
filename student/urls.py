from django.urls import path

from . import views

urlpatterns = [
    path('student-exam-result/<int:student_exam_id>/', views.student_exam_result_view, name='student_exam_result'),
]
