from django.db import models


class FactExamQuestion(models.Model):
    """
    Models ham radio exam questions.
    """

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    ANSWER_CHOICES = (
        (A, A),
        (B, B),
        (C, C),
        (D, D),
    )

    CAT1 = "1"
    CAT2 = "2"
    CAT3 = "3"
    CATEGORY_CHOICES = (
        (CAT1, "Category 1"),
        (CAT2, "Category 2"),
        (CAT2, "Category 3"),
    )

    question = models.TextField()
    answer_a = models.TextField()
    answer_b = models.TextField()
    answer_c = models.TextField()
    answer_d = models.TextField()
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)

    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)

    question_image = models.ImageField(
        upload_to="exams/%Y/%m/",
        max_length=255,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "exam question"
        verbose_name_plural = "exam questions"

    def __str__(self) -> str:
        return str(self.question)
