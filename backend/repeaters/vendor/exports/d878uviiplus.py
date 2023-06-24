"""
Module to generate the files part of the CSV export for the D878UVII+.

On the Anytone D878UVII, names are limited to 16 chars.
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

from repeaters.vendor.utils import rename_duplicates_in_list


class Band2m:
    min = 144.0  # MHz
    max = 146.0  # MHz


class Band70cm:
    min = 430.0  # MHz
    max = 440.0  # MHz


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


class ChannelAnytoneUVIIPlusSerializer:
    """
    Generates Channel.csv as a StringIO.
    """

    def __init__(self):
        """
        Valid channels are the ones that:
            - Are simplex or half-duplex
            - Are in the 2m or 70cm band
            - Are FM or DMR
        """

        def region_and_latitude_sorter(qs):
            return qs.order_by("info_location__region", "-info_location__latitude")

        qs_simplex_2m_fm = region_and_latitude_sorter(
            self._get_repeaters_qs_simplex_2m_fm()
        )
        qs_simplex_2m_dmr = region_and_latitude_sorter(
            self._get_repeaters_qs_simplex_2m_dmr()
        )
        qs_simplex_70cm_fm = region_and_latitude_sorter(
            self._get_repeaters_qs_simplex_70cm_fm()
        )
        qs_simplex_70cm_dmr = region_and_latitude_sorter(
            self._get_repeaters_qs_simplex_70cm_dmr()
        )
        qs_half_duplex_2m_fm = region_and_latitude_sorter(
            self._get_repeaters_qs_half_duplex_2m_fm()
        )
        qs_half_duplex_2m_dmr = region_and_latitude_sorter(
            self._get_repeaters_qs_half_duplex_2m_dmr()
        )
        qs_half_duplex_70cm_fm = region_and_latitude_sorter(
            self._get_repeaters_qs_half_duplex_70cm_fm()
        )
        qs_half_duplex_70cm_dmr = region_and_latitude_sorter(
            self._get_repeaters_qs_half_duplex_70cm_dmr()
        )

        def rename_duplicates_qs_callsign(qs):
            return rename_duplicates_in_list(
                qs.values_list("callsign", flat=True),
                sep=" ",
                start=1,
                update_first=True,
            )

        raw_data = {
            "simplex_2m_fm": {
                "qs": qs_simplex_2m_fm,
                "names": rename_duplicates_qs_callsign(qs_simplex_2m_fm),
            },
            "simplex_2m_dmr": {
                "qs": qs_simplex_2m_dmr,
                "names": rename_duplicates_qs_callsign(qs_simplex_2m_dmr),
            },
            "simplex_70cm_fm": {
                "qs": qs_simplex_70cm_fm,
                "names": rename_duplicates_qs_callsign(qs_simplex_70cm_fm),
            },
            "simplex_70cm_dmr": {
                "qs": qs_simplex_70cm_dmr,
                "names": rename_duplicates_qs_callsign(qs_simplex_70cm_dmr),
            },
            "half_duplex_2m_fm": {
                "qs": qs_half_duplex_2m_fm,
                "names": rename_duplicates_qs_callsign(qs_half_duplex_2m_fm),
            },
            "half_duplex_2m_dmr": {
                "qs": qs_half_duplex_2m_dmr,
                "names": rename_duplicates_qs_callsign(qs_half_duplex_2m_dmr),
            },
            "half_duplex_70cm_fm": {
                "qs": qs_half_duplex_70cm_fm,
                "names": rename_duplicates_qs_callsign(qs_half_duplex_70cm_fm),
            },
            "half_duplex_70cm_dmr": {
                "qs": qs_half_duplex_70cm_dmr,
                "names": rename_duplicates_qs_callsign(qs_half_duplex_70cm_dmr),
            },
        }

        row_counter = 1

        self.data_fm = {}
        for key, value in raw_data.items():
            if key.endswith("_dmr"):
                continue

            self.data_fm[key] = {}

            for index, item in enumerate(value["qs"]):

                # Repeater Tx is radio Rx and vice-versa
                rx_freq = (
                    item.info_simplex.freq_mhz
                    if item.info_simplex
                    else item.info_half_duplex.tx_mhz
                )
                tx_freq = (
                    item.info_simplex.freq_mhz
                    if item.info_simplex
                    else item.info_half_duplex.rx_mhz
                )
                tone = item.info_fm.tone if item.info_fm.tone else 123.0

                self.data_fm[key][row_counter] = {
                    "name": item["names"][index],
                    "rx_freq": rx_freq,
                    "tx_freq": tx_freq,
                    "bandwidth": "12.5K" if item.info_fm.bandwidth=="NFM" else "25K",
                    "tone": tone,
                }

                row_counter += 1

        self.data_dmr = {}
        for key, value in raw_data.items():
            if key.endswith("_fm"):
                continue

            self.data_dmr[key] = {}

            for index, item in enumerate(value["qs"]):

                # Repeater Tx is radio Rx and vice-versa
                rx_freq = (
                    item.info_simplex.freq_mhz
                    if item.info_simplex
                    else item.info_half_duplex.tx_mhz
                )
                tx_freq = (
                    item.info_simplex.freq_mhz
                    if item.info_simplex
                    else item.info_half_duplex.rx_mhz
                )

                if item.info_dmr.ts1_default_tg is not None:
                    ts1_contact = item.info_dmr.ts1_default_tg.name
                    ts1_id = item.info_dmr.ts1_default_tg.id
                else:
                    ts1_contact = "Portugal"
                    ts1_id = "268"
                if item.info_dmr.ts2_default_tg is not None:
                    ts2_contact = item.info_dmr.ts2_default_tg.name
                    ts2_id = item.info_dmr.ts2_default_tg.id
                else:
                    ts2_contact = "Local"
                    ts2_id = "2"

                for ts_n, ts_contact, ts_id, rgl in [
                    ("1", ts1_contact, ts1_id, "TS1 Tipicos"),
                    ("2", ts2_contact, ts2_id, "Todos TGs"),
                ]:
                    self.data_dmr[key][row_counter] = {
                        "name": item["names"][index] + " TS" + ts_n,
                        "rx_freq": rx_freq,
                        "tx_freq": tx_freq,
                        "ts_contact": ts_contact,
                        "ts_id": ts_id,
                        "cc": item.info_dmr.color_code,
                        "ts": ts_n,
                        "rgl": rgl,
                    }

                    row_counter += 1



    def _get_repeaters_qs_simplex_2m(self):
        qs = FactRepeater.objects.filter(
            Q(info_simplex__freq_mhz__gte=Band2m.min)
            & Q(info_simplex__freq_mhz__lte=Band2m.max)
        )

        return qs

    def _get_repeaters_qs_simplex_70cm(self):
        qs = FactRepeater.objects.filter(
            Q(info_simplex__freq_mhz__gte=Band70cm.min)
            & Q(info_simplex__freq_mhz__lte=Band70cm.max)
        )

        return qs

    def _get_repeaters_qs_half_duplex_2m(self):
        # Rx AND Tx between 144.0 and 146.0 MHz
        qs_rx = FactRepeater.objects.filter(
            Q(info_half_duplex__rx_mhz__gte=Band2m.min)
            & Q(info_half_duplex__rx_mhz__lte=Band2m.max)
        )
        qs_tx = FactRepeater.objects.filter(
            Q(info_half_duplex__tx_mhz__gte=Band2m.min)
            & Q(info_half_duplex__tx_mhz__lte=Band2m.max)
        )
        return qs_rx & qs_tx

    def _get_repeaters_qs_half_duplex_70cm(self):
        # Rx AND Tx between 430.0 and 440.0 MHz
        qs_rx = FactRepeater.objects.filter(
            Q(info_half_duplex__rx_mhz__gte=Band70cm.min)
            & Q(info_half_duplex__rx_mhz__lte=Band70cm.max)
        )
        qs_tx = FactRepeater.objects.filter(
            Q(info_half_duplex__tx_mhz__gte=Band70cm.min)
            & Q(info_half_duplex__tx_mhz__lte=Band70cm.max)
        )
        return qs_rx & qs_tx

    def _get_repeaters_qs_simplex_2m_fm(self):
        return self._get_repeaters_qs_simplex_2m().filter(info_fm__isnull=False)

    def _get_repeaters_qs_simplex_70cm_fm(self):
        return self._get_repeaters_qs_simplex_70cm().filter(info_fm__isnull=False)

    def _get_repeaters_qs_half_duplex_2m_fm(self):
        return self._get_repeaters_qs_half_duplex_2m().filter(info_fm__isnull=False)

    def _get_repeaters_qs_half_duplex_70cm_fm(self):
        return self._get_repeaters_qs_half_duplex_70cm().filter(info_fm__isnull=False)

    def _get_repeaters_qs_simplex_2m_dmr(self):
        return self._get_repeaters_qs_simplex_2m().filter(info_dmr__isnull=False)

    def _get_repeaters_qs_simplex_70cm_dmr(self):
        return self._get_repeaters_qs_simplex_70cm().filter(info_dmr__isnull=False)

    def _get_repeaters_qs_half_duplex_2m_dmr(self):
        return self._get_repeaters_qs_half_duplex_2m().filter(info_dmr__isnull=False)

    def _get_repeaters_qs_half_duplex_70cm_dmr(self):
        return self._get_repeaters_qs_half_duplex_70cm().filter(info_dmr__isnull=False)

    def generate_csv(self) -> io.StringIO:
        """
        Generate the CSV file as a StringIO object.
        """

        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Channel Name",
            "Receive Frequency",
            "Transmit Frequency",
            "Channel Type",
            "Transmit Power",
            "Band Width",
            "CTCSS/DCS Decode",
            "CTCSS/DCS Encode",
            "Contact",
            "Contact Call Type",
            "Contact TG/DMR ID",
            "Radio ID",
            "Busy Lock/TX Permit",
            "Squelch Mode",
            "Optional Signal",
            "DTMF ID",
            "2Tone ID",
            "5Tone ID",
            "PTT ID",
            "Color Code",
            "Slot",
            "Scan List",
            "Receive Group List",
            "PTT Prohibit",
            "Reverse",
            "Simplex TDMA",
            "Slot Suit",
            "AES Digital Encryption",
            "Digital Encryption",
            "Call Confirmation",
            "Talk Around(Simplex)",
            "Work Alone",
            "Custom CTCSS",
            "2TONE Decode",
            "Ranging",
            "Through Mode",
            "APRS RX",
            "Analog APRS PTT Mode",
            "Digital APRS PTT Mode",
            "APRS Report Type",
            "Digital APRS Report Channel",
            "Correct Frequency[Hz]",
            "SMS Confirmation",
            "Exclude channel from roaming",
            "DMR MODE",
            "DataACK Disable",
            "R5toneBot",
            "R5ToneEot",
            "Auto Scan",
            "Ana Aprs Mute",
            "Send Talker Alias",
        ]

        writer.writerow(header)

        pass # TODO(ruilvo): implement
