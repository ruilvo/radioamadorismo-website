import io

from django.views.decorators.http import require_safe
from django.http import HttpRequest, HttpResponse

from .exports.d878uvii import (
    tgs_csv,
    receive_groups_csv,
)


def generate_csv_response(filename: str, content: io.StringIO) -> HttpResponse:
    response = HttpResponse(content.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = f'attachment;filename="{filename}"'

    return response


@require_safe
def d878uvii_tgs_view(request: HttpRequest):
    return generate_csv_response("TalkGroups.csv", tgs_csv())


@require_safe
def d878uvii_rgs_view(request: HttpRequest):
    return generate_csv_response("ReceiveGroupCallList.csv", receive_groups_csv())
