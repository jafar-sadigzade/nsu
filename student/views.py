from django.shortcuts import render, get_object_or_404

from .models import StudentExamResult


def student_exam_result_view(request, student_exam_id):
    # Fetch the StudentExamResult by its ID
    student_exam_result = get_object_or_404(StudentExamResult, id=student_exam_id)

    # Get the student data
    student_data = student_exam_result.student_data

    # Pass the student_data to the template
    return render(request, 'student_exam_result.html', {
        'student_data': student_data
    })
