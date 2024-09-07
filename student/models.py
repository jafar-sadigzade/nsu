from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def is_check_student_id(student_id):
    if len(student_id) != 7:
        raise ValidationError(f'İş nömrəsi 7 simvol olmalıdır!\nSiz {len(student_id)} simvol daxil etdiniz!')


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Şagird",
        help_text="Birinci olaraq şagird <istifadəçi> olaraq yaradılmalıdır!"
    )
    student_id = models.IntegerField(
        unique=True,
        verbose_name="İş nömrəsi",
        help_text="7 simvollu ədəd daxil edilməlidir!",
        validators=[is_check_student_id]
    )

    def __str__(self):
        return f"İş nömrəsi: {self.student_id} -> {self.user.full_name()}"

    class Meta:
        verbose_name = "Şagird"
        verbose_name_plural = "Şagirdlər"
        indexes = [
            models.Index(fields=['student_id']),
        ]


class StudentExamResult(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='student_exam_results',
        verbose_name="Şagird",
        help_text="Dəyişiklik etməyin"
    )
    exam = models.ForeignKey(
        'exam.Exam',
        on_delete=models.CASCADE,
        verbose_name="İmtahan",
        help_text="Dəyişiklik etməyin"
    )
    answers_json = models.JSONField(
        default=dict,
        verbose_name="İmtahan formasından gələnlər",
        help_text="Dəyişiklik etməyin"
    )
    student_answers_json = models.JSONField(
        default=dict,
        verbose_name="TXT-dən gələnlər",
        help_text="Dəyişiklik etməyin"
    )

    @property
    def student_data(self):
        student_data = {**self.student_answers_json}
        student_data.pop("answers", {})

        answers_list = [v for v in self.student_answers_json.get("answers", {}).values()]
        student_data["student_answers"] = ','.join(answers_list)

        subjects = {}
        for idx, subject in enumerate(self.answers_json, 1):
            question_types = []
            for qt in subject["question_type"]:
                qt_data = {
                    "type_code": qt["type_code"],
                    "points_per_correct": qt["points_per_correct"],
                    "points_per_incorrect": qt["points_per_incorrect"],
                    "number_of_questions": qt["number_of_questions"],
                    "number_of_symbols": qt["number_of_symbols"]
                }

                if qt["type_code"] == "qs":
                    qt_data["correct_answers"] = subject["answers"][:qt["number_of_questions"]]
                elif qt["type_code"] == "k":
                    qt_data["correct_answers"] = subject["answers"][
                                                 len(subject["answers"]) - (qt["number_of_symbols"] + 1) * qt[
                                                     "number_of_questions"]:]
                else:
                    qt_data["answers"] = {
                        f"answer{num + 1}": 0 for num in range(qt["number_of_questions"])
                    }

                question_types.append(qt_data)

            subjects[f"subjects{idx}"] = {
                "subject_name": subject["subject_name"],
                "question_type": question_types
            }

        student_data["subjects"] = subjects
        return student_data

    def __str__(self):
        return f"{self.student.user.full_name()} - {self.student.student_id} - {self.exam.name}"

    class Meta:
        verbose_name = "Şagird imtahan nəticələri"
        verbose_name_plural = verbose_name
