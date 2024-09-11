import json

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def is_check_student_id(student_id):
    if len(student_id) != 7:
        raise ValidationError(
            _('İş nömrəsi 7 simvol olmalıdır!\nSiz %(length)d simvol daxil etdiniz!'),
            params={'length': len(student_id)},
        )


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Şagird",
        help_text="Birinci olaraq şagird <istifadəçi> olaraq yaradılmalıdır!"
    )
    student_id = models.CharField(
        max_length=7,
        unique=True,
        verbose_name="İş nömrəsi",
        help_text="7 simvollu ədəd daxil edilməlidir!",
        validators=[is_check_student_id]
    )

    def __str__(self):
        return f"İş nömrəsi: {self.student_id} -> {self.user.get_full_name()}"

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
        # Mapping for foreign language codes
        foreign_language_map = {
            "I": "İngilis dili",
            "F": "Fransız dili",
            "A": "Alman dili",
            "R": "Rus dili"
        }

        # Merge student_answers_json and remove 'answers' key
        student_data = {**self.student_answers_json}
        student_data.pop("answers", None)

        # Update "Xarici dil" field with full language name
        foreign_lang_code = student_data.get("Xarici dil")
        if foreign_lang_code in foreign_language_map:
            student_data["Xarici dil"] = foreign_language_map[foreign_lang_code]
        else:
            student_data["Xarici dil"] = "Unknown"

        # Prepare student answers list and join with commas
        answers_list = [v for v in self.student_answers_json.get("answers", {}).values()]
        student_data["student_answers"] = ','.join(answers_list)

        # Initialize total scores
        total_scores = 0

        # Prepare subjects and their question types, remove other foreign language subjects
        subjects = {}
        for idx, subject in enumerate(self.answers_json, 1):
            # If the subject is a foreign language other than the student's chosen one, skip it
            if (subject["subject_name"] in ["Fransız dili", "Alman dili", "Rus dili", "İngilis dili"]
                    and subject["subject_name"] != student_data["Xarici dil"]):
                continue

            # Initialize subject metrics
            number_of_correct_answers = 0
            number_of_wrong_answers = 0

            question_types = []
            student_answers = student_data.get("student_answers", "")
            answer_index = 0

            for qt in subject["question_type"]:
                subject_total_scores = 0
                qt_data = {
                    "type_code": qt["type_code"],
                    "points_per_correct": qt["points_per_correct"],
                    "points_per_incorrect": qt["points_per_incorrect"],
                    "number_of_questions": qt["number_of_questions"],
                }

                # Handle question type specific answers logic
                if qt["type_code"] == "qs":
                    correct_answers = subject["answers"][:qt["number_of_questions"]]
                    for _ in range(qt["number_of_questions"]):
                        if answer_index >= len(student_answers):
                            break
                        student_answer = student_answers[answer_index]
                        correct_answer = correct_answers[_]
                        if student_answer == correct_answer or correct_answer == '*':
                            number_of_correct_answers += 1
                        elif student_answer != ' ':
                            number_of_wrong_answers += 1
                        answer_index += 1
                    if qt_data["points_per_incorrect"] != 0:
                        question_type_total_scores = (number_of_correct_answers - (
                                number_of_wrong_answers / qt_data["points_per_incorrect"])) * qt_data[
                                                   "points_per_correct"]
                    else:
                        question_type_total_scores = number_of_correct_answers * qt_data["points_per_correct"]
                    qt_data["correct_answers"] = correct_answers
                    qt_data["number_of_correct_answers"] = number_of_correct_answers
                    qt_data["number_of_wrong_answers"] = number_of_wrong_answers
                    qt_data["question_type_total_scores"] = question_type_total_scores
                elif qt["type_code"] == "k":
                    qt_data["number_of_symbols"] = qt["number_of_symbols"]
                    start_idx = -(qt["number_of_symbols"] + 1) * qt["number_of_questions"]
                    qt_data["correct_answers"] = subject["answers"][start_idx:]
                    question_type_total_scores = 0
                    qt_data["number_of_correct_answers"] = number_of_correct_answers
                    qt_data["number_of_wrong_answers"] = number_of_wrong_answers
                    qt_data["question_type_total_scores"] = question_type_total_scores
                else:
                    qt_data["answers"] = {f"answer{num + 1}": 0 for num in range(qt["number_of_questions"])}
                    question_type_total_scores = 0

                question_types.append(qt_data)
                # Calculate subject total score
                subject_total_scores += question_type_total_scores
                total_scores += subject_total_scores

                subjects[f"subject_{idx}"] = {
                    "subject_name": subject["subject_name"],
                    "subject_order": subject["subject_order"],
                    "subject_total_scores": subject_total_scores,
                    "question_type": question_types
                }

        # Add subjects and total_scores to student data
        student_data["subjects"] = subjects
        student_data["total_scores"] = total_scores

        # Return JSON string with double quotes
        return json.dumps(student_data, ensure_ascii=False)

    def __str__(self):
        return f"{self.id} - {self.student.user.get_full_name() or 'No Name'} - {self.student.student_id} - {self.exam.name}"

    class Meta:
        verbose_name = "Şagird imtahan nəticələri"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['student']),
            models.Index(fields=['exam']),
        ]
