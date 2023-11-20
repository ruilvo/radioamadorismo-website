"""
Define the Django views for the repeaters app
"""

from django.views.decorators.http import require_safe
from django.http import HttpRequest

from portal.responses import generate_csv_response, generate_zip_response

from repeaters.exports.anytone_d878uviip import (
    DimDmrTgAnytoneUVIIPlusSerializer,
    ReceiveGroupCallListAnytoneUVIIPlusSerializer,
    ChannelAnytoneUVIIPlusSerializer,
    ZoneAnytoneUVIIPlusSerializer,
    codeplug_zip,
)

from repeaters.exports.chirp import chirp_csv


@require_safe
def d878uvii_tgs_view(_: HttpRequest):
    return generate_csv_response(
        "TalkGroups.csv", DimDmrTgAnytoneUVIIPlusSerializer().generate_csv()
    )


@require_safe
def d878uvii_rgs_view(_: HttpRequest):
    return generate_csv_response(
        "ReceiveGroupCallList.csv",
        ReceiveGroupCallListAnytoneUVIIPlusSerializer(
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


@require_safe
def chirp_csv_view(_: HttpRequest):
    return generate_csv_response("chirp.csv", chirp_csv())
