import json

from django.db import models


class QuestionType(models.Model):
    TYPE_CHOICES = [
        ('qs', 'Qapalı sual'),
        ('as', 'Açıq sual'),
        ('k', 'Ənənəvi kodlaşdırılan'),
        ('us', 'Uyğunluq sualı'),
        ('ss', 'Situasiya'),
    ]

    name = models.CharField(
        max_length=50,
        verbose_name="Sual tipinin adı",
        help_text="Maksimum 50 simvol"
    )
    type_code = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        verbose_name="Sual tipi",
        help_text="Birini seçin"
    )
    points_per_correct = models.FloatField(
        default=0,
        verbose_name="Düz sual üçün təyin olunan bal",
        help_text="Onluq ədəd seçilə bilər (vergüldən sonra 2 ədəd)",
    )
    points_per_incorrect = models.PositiveIntegerField(
        default=0,
        verbose_name="Neçə səhv bir düzü aparsın",
        help_text="Natural ədəd daxil edin\nƏgər aparmayacaqsa 0 olaraq qalsın.",
    )
    number_of_questions = models.PositiveIntegerField(
        default=0,
        verbose_name="Sual sayı",
        help_text="Müsbət ədəd daxil edin"
    )
    number_of_symbols = models.PositiveIntegerField(
        default=0,
        verbose_name="Simvol sayı",
        help_text="Sadəcə açıq suallarda simvol sayını yazmaq kifayətdir!"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıra nömrəsi",
        help_text="Sual tipinin sırası (azdan çoxa doğru sıralanır)"
    )

    def __str__(self):
        return f"{self.number_of_questions} - {self.name} - {self.points_per_correct} bal - {self.points_per_incorrect} səhv 1 düzü aparır"

    class Meta:
        verbose_name = 'Sual tipi'
        verbose_name_plural = 'Sual tipləri'
        indexes = [
            models.Index(fields=['order']),
        ]


class Subject(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Fənnin adı",
        help_text="Maksimum 100 simvol"
    )
    questions = models.ManyToManyField(
        QuestionType,
        verbose_name="Sual tipi",
        help_text="Biri və ya bir neçəsi seçilə bilər"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sıra nömrəsi",
        help_text="Fənnin sırası (azdan çoxa doğru sıralanır)"
    )
    is_foreign_language = models.BooleanField(
        default=False,
        verbose_name="Xarici dildirmi",
        help_text="Daxil etdiyiniz fənn xarici dildirsə klikləyin"
    )
    foreign_language_code = models.CharField(
        max_length=1,
        verbose_name="Xarici dilin kodu",
        help_text="Cavab kartında yazanlardan biri.\n Nümunə: IFAR",
        blank=True,
    )

    def __str__(self):
        question_types = ", ".join([str(question) for question in self.questions.order_by('order')])
        return f"{self.name} - {question_types}"

    class Meta:
        verbose_name = 'Fənn'
        verbose_name_plural = 'Fənlər'


class ExamType(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="İmtahan tipinin adı",
        help_text="Maksimum 255 simvol"
    )
    subjects = models.ManyToManyField(
        Subject,
        verbose_name="Fənnlər",
        help_text="Biri və ya bir neçəsi seçilə bilər"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "İmtahan tipi"
        verbose_name_plural = verbose_name


class ColumnMapping(models.Model):
    exam_type = models.ForeignKey(
        ExamType,
        on_delete=models.CASCADE,
        verbose_name="İmtahan tipi"
    )
    column_id = models.PositiveIntegerField(
        verbose_name="Sütun nömrəsi",
        help_text="Optik oxuyucudan çıxan txt-ə bax!"
    )
    column_name = models.CharField(
        max_length=255,
        verbose_name="Sütun adı",
        help_text="Maksimum 255 simvol"
    )
    is_answers = models.BooleanField(
        default=False,
        verbose_name="Şagird cavabları olan sütun",
        help_text="Əgər bu sütun cavablardırsa onda klikləyin"
    )

    def __str__(self):
        return self.column_name

    class Meta:
        verbose_name = "Sütun xəritələmə"
        verbose_name_plural = verbose_name
        indexes = [
            models.Index(fields=['exam_type', 'column_id']),
        ]


class Exam(models.Model):
    exam_type = models.ForeignKey(
        ExamType,
        verbose_name="İmtahan tipi",
        help_text="Mütləq seçilməlidir",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=255,
        verbose_name="İmtahan adı",
        help_text="Maksimum 255 simvol"
    )
    students_answers_txt = models.FileField(
        upload_to="exams/omr/",
        verbose_name="Optik oxuyucu şagird nəticələri",
        help_text="Mütləq daxil edilməlidir(.txt formatında)"
    )
    correct_answers_txt = models.FileField(
        upload_to="exams/answers/",
        verbose_name="Düzgün cavablar",
        help_text="Optik oxuyucudan çıxan forma ilə eyni şəkildə hazırlanmalıdır",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Yaradılma tarixi",
        help_text="İmtahan daxil ediləndəki tarix və saat. Redakte etmək mümkün deyil!"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Dəyişdirilmə tarixi",
        help_text="Sonuncu yaddaşa vermə tarixi və saatı. Redakte etmək mümkün deyil!"
    )

    def __str__(self):
        return self.name

    @property
    def answers_json(self):
        if not self.correct_answers_txt:
            return []

        try:
            # Read file content
            with self.correct_answers_txt.open('r') as file:
                file_content = file.read().strip()
        except Exception as e:
            raise f"Error reading file: {e}"

        if not file_content:
            return []

        # Split file content into answers
        subjects_answers = [answer for answer in file_content.split(',') if answer]

        # Fetch subjects and prepare JSON
        subjects = self.exam_type.subjects.all().order_by('order')
        result = []

        for i, subject in enumerate(subjects):
            if i >= len(subjects_answers):
                break

            question_types = subject.questions.all()
            question_types_data = []
            for question_type in question_types:
                question_types_data.append({
                    "type_code": question_type.type_code,
                    "points_per_correct": question_type.points_per_correct,
                    "points_per_incorrect": question_type.points_per_incorrect,
                    "number_of_questions": question_type.number_of_questions,
                    "number_of_symbols": question_type.number_of_symbols
                })

            result.append({
                "subject_name": subject.name,
                "question_type": question_types_data,
                "answers": subjects_answers[i]
            })

        return json.dumps(result, ensure_ascii=False, indent=4)

    @staticmethod
    def replace_special_characters(text):
        replacements = {
            "u": "Ü",
            "o": "Ö",
            "g": "Ğ",
            "i": "I",
            "e": "Ə",
            "c": "Ç",
            "s": "Ş",
        }

        for key, value in replacements.items():
            text = text.replace(key, value)

        return text

    @property
    def student_answers_json(self):
        if not self.students_answers_txt:
            print("No file provided.")
            return []

        try:
            # Read file content
            with self.students_answers_txt.open('r') as file:
                file_content = file.readlines()
            print(f"File Content: {file_content}")  # Debug print
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

        if not file_content:
            print("File content is empty.")
            return []

        # Create column mapping dictionary
        column_mapping = {
            column.column_id: column
            for column in ColumnMapping.objects.filter(exam_type=self.exam_type)
        }
        print(f"Column Mapping: {column_mapping}")  # Debug print

        results = []

        for line in file_content:
            columns = line.strip().split(',')
            result = {}
            answers = {}

            for column_id, column in column_mapping.items():
                if column_id < len(columns):
                    value = columns[column_id].strip()  # Ensure there's no trailing whitespace
                    if column.is_answers:
                        answers[column.column_name] = value
                    else:
                        result[column.column_name] = self.replace_special_characters(value)

            # Add answers to result if any
            if answers:
                result['answers'] = answers

            results.append(result)

        print(f"Result JSON: {results}")  # Debug print
        return json.dumps(results, ensure_ascii=False, indent=4)

    class Meta:
        verbose_name = "İmtahan"
        verbose_name_plural = "İmtahanlar"
        indexes = [
            models.Index(fields=['exam_type']),
        ]
