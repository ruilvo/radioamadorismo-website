"""
Define the Django views for the repeaters app
"""

from django.views.decorators.http import require_safe
from django.http import HttpRequest

from portal.responses import generate_csv_response, generate_zip_response

from repeaters.exports.chirp import chirp_csv


@require_safe
def chirp_csv_view(_: HttpRequest):
    return generate_csv_response("chirp.csv", chirp_csv())
