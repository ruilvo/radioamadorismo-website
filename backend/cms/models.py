from django.core.validators import FileExtensionValidator
from django.db import models


class FactPdf(models.Model):
    """
    Model to store records of uploaded PDFs to the server
    """

    title = models.CharField(max_length=255)
    file = models.ImageField(
        upload_to="pdfs/%Y/%m/",
        max_length=255,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def __str__(self):
        return self.title


class FactImage(models.Model):
    """
    Model to store records of uploaded images to the server
    """

    title = models.CharField(max_length=255)
    width = models.PositiveIntegerField(editable=False)
    height = models.PositiveIntegerField(editable=False)
    file = models.ImageField(
        upload_to="images/%Y/%m/",
        height_field="height",
        width_field="width",
        max_length=255,
    )

    def __str__(self):
        return self.title


class FactBlogPost(models.Model):
    """
    Model to store records of blog posts.
    """

    title = models.CharField(max_length=255)
    intro = models.TextField()
    body = models.TextField()
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
