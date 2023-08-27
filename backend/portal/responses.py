"""
Create HTTP responses for random types of files
"""

import io
from django.http import HttpResponse


def generate_csv_response(filename: str, content: io.StringIO) -> HttpResponse:
    response = HttpResponse(content.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = f'attachment;filename="{filename}"'

    return response


def generate_zip_response(filename: str, content: io.BytesIO) -> HttpResponse:
    response = HttpResponse(content.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment;filename="{filename}"'

    return response
