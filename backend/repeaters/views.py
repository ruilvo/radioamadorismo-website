"""
Define the Django views for the repeaters app
"""

import io

from django.views.decorators.http import require_safe
from django.http import HttpRequest, HttpResponse

from repeaters.vendor.exports.anytone_d878uviip import (
    DimDmrTgAnytoneUVIIPlusSerializer,
    ReceiveGroupsAnytoneUVIIPlusSerializer,
    ChannelAnytoneUVIIPlusSerializer,
    ZoneAnytoneUVIIPlusSerializer,
    codeplug_zip,
)


def generate_csv_response(filename: str, content: io.StringIO) -> HttpResponse:
    response = HttpResponse(content.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = f'attachment;filename="{filename}"'

    return response


def generate_zip_response(filename: str, content: io.BytesIO) -> HttpResponse:
    response = HttpResponse(content.getvalue(), content_type="application/zip")
    response["Content-Disposition"] = f'attachment;filename="{filename}"'

    return response


@require_safe
def d878uvii_tgs_view(_: HttpRequest):
    return generate_csv_response(
        "TalkGroups.csv", DimDmrTgAnytoneUVIIPlusSerializer().generate_csv()
    )


@require_safe
def d878uvii_rgs_view(_: HttpRequest):
    return generate_csv_response(
        "ReceiveGroupCallList.csv",
        ReceiveGroupsAnytoneUVIIPlusSerializer(
            DimDmrTgAnytoneUVIIPlusSerializer()
        ).generate_csv(),
    )


@require_safe
def d878uvii_channels_view(_: HttpRequest):
    return generate_csv_response(
        "Channel.csv", ChannelAnytoneUVIIPlusSerializer().generate_csv()
    )


@require_safe
def d878uvii_zones_view(_: HttpRequest):
    return generate_csv_response(
        "Zone.csv",
        ZoneAnytoneUVIIPlusSerializer(
            ChannelAnytoneUVIIPlusSerializer()
        ).generate_csv(),
    )


@require_safe
def d878uvii_codeplug_view(_: HttpRequest):
    return generate_zip_response("codeplug.zip", codeplug_zip())
