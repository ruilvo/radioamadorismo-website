"""
Module to generate the files part of the CSV export for the D878UVII+.

On the Anytone D878UVII+, names are limited to 16 chars.
"""

import io
import csv

from typing import Tuple, List, Dict

from django.db.models import Q
from django.db.models.query import QuerySet

from repeaters.models import (
    DimDmr,
    DimDmrTg,
    FactRepeater,
)

from repeaters.vendor.bands import Band2m, Band70cm

from repeaters.vendor.utils import rename_duplicates_in_list


class D878UVIIPlusDialect(csv.excel):
    quotechar = '"'
    quoting = csv.QUOTE_ALL


csv.register_dialect("d878uviiplus", D878UVIIPlusDialect)


def radio_id_csv() -> io.StringIO:
    """
    Generates a placeholder RadioIDList.csv
    """

    header = ["No.", "Radio ID", "Name"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    placeholder_radio_id = ("1", "268000", "CT0ZZZ")
    writer.writerow(
        [
            f"{placeholder_radio_id[0]}",
            f"{placeholder_radio_id[1]}",
            f"{placeholder_radio_id[2]}",
        ]
    )

    return sio


def scanlist_csv() -> io.StringIO:
    """
    Generates a placeholder ScanList.csv
    """

    header = [
        "No.",
        "Scan List Name",
        "Scan Channel Member",
        "Scan Channel Member RX Frequency",
        "Scan Channel Member TX Frequency",
        "Scan Mode",
        "Priority Channel Select",
        "Priority Channel 1",
        "Priority Channel 1 RX Frequency",
        "Priority Channel 1 TX Frequency",
        "Priority Channel 2",
        "Priority Channel 2 RX Frequency",
        "Priority Channel 2 TX Frequency",
        "Revert Channel",
        "Look Back Time A[s]",
        "Look Back Time B[s]",
        "Dropout Delay Time[s]",
        "Dwell Time[s]",
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio


def roamingzone_csv() -> io.StringIO:
    """
    Generates a placeholder RoamingZone.csv
    """

    header = [
        "No.",
        "Name",
        "Roaming Channel Member",
        "",
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio


def roaming_channel_csv() -> io.StringIO:
    """
    Generates a placeholder RoamingChannel.csv
    """

    header = [
        "No.",
        "Receive Frequency",
        "Transmit Frequency",
        "Color Code",
        "Slot",
        "Name",
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    return sio


class DimDmrTgAnytoneUVIIPlusSerializer:
    """
    Generates the CSV file for the D878UVII+ with the DMR talkgroups.
    """

    def __init__(self):
        qs = DimDmrTg.objects.all()

        # Generate the data to be written to the CSV file
        names = qs.values_list("name", flat=True)
        names = rename_duplicates_in_list(names, sep=" ", start=1, update_first=True)
        self.data = {}
        for tg in qs:
            self.data[tg.pk] = {
                "id": tg.id,
                "name": tg.name,
                "type": tg.call_mode,
            }

    def generate_csv(self) -> io.StringIO:
        """
        Generate the CSV file as a StringIO object.
        """

        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Radio ID", "Name", "Call Type", "Call Alert"]
        writer.writerow(header)

        for index, item in enumerate(self.data.values()):
            writer.writerow(
                [
                    f"{index}",
                    f"{item['id']}",
                    f"{item['name']}",
                    f"{'Group Call' if item['type'] == 'GROUP_CALL' else 'Private Call'}",
                    "None",  # Call Alert
                ]
            )

        return sio


class ReceiveGroupsAnytoneUVIIPlusSerializer:
    """
    Generates `ReceiveGroupCallList.csv` as a StringIO.

    We'll be generating 2 groups:
     - The expected TS1 slot TGs
     - All TGs
    """

    def __init__(self, tg_serializer: DimDmrTgAnytoneUVIIPlusSerializer):
        ts1_default_tgs_qs = DimDmrTg.objects.filter(
            dimdmr_ts1_default_tg__isnull=False
        )
        ts1_alternative_tgs_qs = DimDmrTg.objects.filter(
            dimdmr_ts1_alternative_tgs__in=DimDmr.objects.all()
        )

        ts1_tgs_qs = (ts1_default_tgs_qs | ts1_alternative_tgs_qs).distinct()
        tgs_qs = DimDmrTg.objects.all()

        self.data = {}
        for index, (name, qs) in enumerate(
            zip(["TS1 TGs", "Todos TGs"], [ts1_tgs_qs, tgs_qs])
        ):
            self.data[index + 1] = {
                "name": name,
                "contacts": [tg_serializer.data[tg.pk]["name"] for tg in qs],
                "ids": [tg_serializer.data[tg.pk]["id"] for tg in qs],
            }

    def generate_csv(self) -> io.StringIO:
        """
        Generate the CSV file as a StringIO object.
        """

        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Group Name", "Contact", "Contact TG/DMR ID"]
        writer.writerow(header)

        for index, item in self.data.items():
            writer.writerow(
                [
                    f"{index}",
                    f"{item['name']}",
                    f"{'|'.join(item['contacts'])}",
                    f"{'|'.join(item['ids'])}",
                ]
            )

        return sio
