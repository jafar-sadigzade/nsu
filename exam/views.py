from django.http import HttpResponse
from exam.models import ExamType, Exam


def test(request):
    json = Exam.objects.all()
    context = [
        json[0].exam_details_json
    ]
    return HttpResponse(context)
