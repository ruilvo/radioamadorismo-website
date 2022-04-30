from django.views.decorators.http import require_safe
from django.http import HttpRequest, HttpResponse

from .exports.d878uvii import (
    tgs_csv,
    receive_groups_csv,
)


@require_safe
def d878uvii_tgs_view(request: HttpRequest):

    tg_file = tgs_csv().getvalue()

    response = HttpResponse(tg_file, content_type="text/csv")
    response["Content-Disposition"] = 'attachment;filename="TalkGroups.csv"'

    return response


@require_safe
def d878uvii_rgs_view(request: HttpRequest):

    rgs_file = receive_groups_csv().getvalue()

    response = HttpResponse(rgs_file, content_type="text/csv")
    response["Content-Disposition"] = 'attachment;filename="ReceiveGroupCallList.csv"'

    return response
