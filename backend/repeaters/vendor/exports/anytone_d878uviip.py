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
    DimLocation,
    DimRf,
    DimFm,
    DimDmrTg,
    FactRepeater,
)

from repeaters.vendor.utils import rename_duplicates_in_list


class D878UVIIPlusDialect(csv.excel):
    quotechar = '"'
    quoting = csv.QUOTE_ALL


csv.register_dialect("d878uviiplus", D878UVIIPlusDialect)


# 2ToneEncode.CSV  -> Not needed
# 5ToneEncode.CSV  -> Not needed
# AESEncryptionCode.CSV  -> Not needed
# APRS.CSV  -> TODO or not?
# AR4EncryptionCode.CSV  -> Not needed
# AnalogAddressBook.CSV  -> Not needed
# AutoRepeaterOffsetFrequencys.CSV  -> Done
# Channel.CSV
# DTMFEncode.CSV  -> Not needed
# DigitalContactList.CSV  -> Won't do
# FM.CSV  -> Not needed
# GPSRoaming.CSV  -> Won't do for now
# HotKey_HotKey.CSV  -> Not needed
# HotKey_QuickCall.CSV  -> Not needed
# HotKey_State.CSV  -> Not needed
# PrefabricatedSMS.CSV  -> Not needed
# RadioIDList.CSV  -> Done as a placeholder
# ReceiveGroupCallList.CSV  -> Done
# RoamingChannel.CSV  -> Done as a placeholder
# RoamingZone.CSV  -> Done as a placeholder
# ScanList.CSV  -> Done as a placeholder
# TalkGroups.CSV  -> Done
# Zone.CSV
# codeplug.LST  -> TODO


def radioidlist_csv() -> io.StringIO:
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


def roamingchannel_csv() -> io.StringIO:
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


def autorepeateroffsetfrequencys_csv() -> io.StringIO:
    """
    Generates a placeholder AutoRepeaterOffsetFrequencys.csv
    """

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")

    writer.writerow(["No.", "Offset Frequency"])
    writer.writerow(["1", "600.00 KHz"])
    writer.writerow(["2", "7.60000 MHz"])

    return sio


class DimDmrTgAnytoneUVIIPlusSerializer:
    """
    Generates the TalkGroups.csv CSV file for the D878UVII+ with the DMR talkgroups.
    """

    def __init__(self):
        qs = DimDmrTg.objects.all().order_by("id")

        # Generate the data to be written to the CSV file
        self.data = {}
        for tg in qs:
            self.data[tg.pk] = {
                "id": tg.id,
                "name": tg.name,
                "type": tg.call_mode,
            }

    def generate_csv(self) -> io.StringIO:
        """
        Generate the TalkGroups.csv file as a StringIO object.
        """

        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Radio ID", "Name", "Call Type", "Call Alert"]
        writer.writerow(header)

        for index, item in enumerate(self.data.values()):
            writer.writerow(
                [
                    f"{index+1}",  # Needs to be 1-indexed
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

    We'll be generating a single group with all the talkgroups to keep it simple.
    """

    def __init__(self, tg_serializer: DimDmrTgAnytoneUVIIPlusSerializer):
        self.data = {}
        for index, elem in enumerate(tg_serializer.data.values()):
            self.data[index + 1] = {
                "id": elem["id"],
                "contact": elem["name"],
            }

    def generate_csv(self) -> io.StringIO:
        """
        Generate the CSV file as a StringIO object.
        """

        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = ["No.", "Group Name", "Contact", "Contact TG/DMR ID"]
        writer.writerow(header)

        values = self.data.values()
        contacts = [item["contact"] for item in values]
        ids = [str(item["id"]) for item in values]

        writer.writerow(
            [
                "1",
                "Todos TGs",
                f"{'|'.join(contacts)}",
                f"{'|'.join(ids)}",
            ]
        )

        return sio


class ChannelAnytoneUVIIPlusSerializer:
    """
    Generates `Channel.csv` as a StringIO.
    """

    def __init__(self):
        """
        Let's generate the data according to these rules:

        Continent 2m FM, sorted by descending latitude
        Continent 70cm FM, sorted by descending latitude
        Continent 2m DMR, sorted by descending latitude
        Continent 70cm DMR, sorted by descending latitude
        Madeira 2m FM, sorted by ascending longitude
        Madeira 70cm FM, sorted by ascending longitude
        Madeira 2m DMR, sorted by ascending longitude
        Madeira 70cm DMR, sorted by ascending longitude
        Azores 2m FM, sorted by ascending longitude
        Azores 70cm FM, sorted by ascending longitude
        Azores 2m DMR, sorted by ascending longitude
        Azores 70cm DMR, sorted by ascending longitude
        """

        # Generate the querysets for the data that is going to be written to the CSV file
        qss = {
            "continent_2m_fm": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.CONTINENT)
                & Q(info_rf__band=DimRf.BandOptions.B_2M)
                & Q(modes__contains=[FactRepeater.ModeOptions.FM])
            ).order_by("-info_location__latitude"),
            "continent_70cm_fm": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.CONTINENT)
                & Q(info_rf__band=DimRf.BandOptions.B_70CM)
                & Q(modes__contains=[FactRepeater.ModeOptions.FM])
            ).order_by("-info_location__latitude"),
            "continent_2m_dmr": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.CONTINENT)
                & Q(info_rf__band=DimRf.BandOptions.B_2M)
                & Q(modes__contains=[FactRepeater.ModeOptions.DMR])
            ).order_by("-info_location__latitude"),
            "continent_70cm_dmr": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.CONTINENT)
                & Q(info_rf__band=DimRf.BandOptions.B_70CM)
                & Q(modes__contains=[FactRepeater.ModeOptions.DMR])
            ).order_by("-info_location__latitude"),
            "madeira_2m_fm": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.MADEIRA)
                & Q(info_rf__band=DimRf.BandOptions.B_2M)
                & Q(modes__contains=[FactRepeater.ModeOptions.FM])
            ).order_by("info_location__longitude"),
            "madeira_70cm_fm": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.MADEIRA)
                & Q(info_rf__band=DimRf.BandOptions.B_70CM)
                & Q(modes__contains=[FactRepeater.ModeOptions.FM])
            ).order_by("info_location__longitude"),
            "madeira_2m_dmr": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.MADEIRA)
                & Q(info_rf__band=DimRf.BandOptions.B_2M)
                & Q(modes__contains=[FactRepeater.ModeOptions.DMR])
            ).order_by("info_location__longitude"),
            "madeira_70cm_dmr": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.MADEIRA)
                & Q(info_rf__band=DimRf.BandOptions.B_70CM)
                & Q(modes__contains=[FactRepeater.ModeOptions.DMR])
            ).order_by("info_location__longitude"),
            "azores_2m_fm": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.AZORES)
                & Q(info_rf__band=DimRf.BandOptions.B_2M)
                & Q(modes__contains=[FactRepeater.ModeOptions.FM])
            ).order_by("info_location__longitude"),
            "azores_70cm_fm": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.AZORES)
                & Q(info_rf__band=DimRf.BandOptions.B_70CM)
                & Q(modes__contains=[FactRepeater.ModeOptions.FM])
            ).order_by("info_location__longitude"),
            "azores_2m_dmr": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.AZORES)
                & Q(info_rf__band=DimRf.BandOptions.B_2M)
                & Q(modes__contains=[FactRepeater.ModeOptions.DMR])
            ).order_by("info_location__longitude"),
            "azores_70cm_dmr": FactRepeater.objects.filter(
                Q(info_location__region=DimLocation.RegionOptions.AZORES)
                & Q(info_rf__band=DimRf.BandOptions.B_70CM)
                & Q(modes__contains=[FactRepeater.ModeOptions.DMR])
            ).order_by("info_location__longitude"),
        }

        # Create the data to be written to the CSV file
        count = 0
        self.data = {}
        for key, qs in qss.items():
            self.data[key] = []
            for elem in qs:
                count += 1
                current_data = {
                    "no": f"{count}",
                    # Repeater Tx is radio Rx
                    "rx": f"{elem.info_rf.tx_mhz:.5f}",
                    # and vice-versa
                    "tx": f"{elem.info_rf.rx_mhz:.5f}",
                }
                if "fm" in key:
                    # Generate data for FM repeaters
                    bw = (
                        "12.5K"
                        if elem.info_fm.bandwidth == DimFm.BandwidthOptions.NFM
                        else "25K"
                    )
                    current_data |= {
                        "name": elem.callsign,
                        "bw": bw,
                        "ctcss": f"{elem.info_fm.tone:.1f}",
                    }
                    self.data[key].append(current_data)
                elif "dmr" in key:
                    # Generate data for DMR repeaters
                    color_code = str(elem.info_dmr.color_code)
                    for ts_n in [1, 2]:
                        ts = f"TS{ts_n}"
                        contact = elem.info_dmr.ts1_default_tg.name
                        contact_call_type = (
                            "Group Call"
                            if elem.info_dmr.ts1_default_tg.call_mode
                            == DimDmrTg.CallModeOptions.GROUP_CALL
                            else "Private Call"
                        )
                        contact_id = elem.info_dmr.ts1_default_tg.id
                        if ts == "TS2":
                            contact = elem.info_dmr.ts2_default_tg.name
                            contact_call_type = (
                                "Group Call"
                                if elem.info_dmr.ts2_default_tg.call_mode
                                == DimDmrTg.CallModeOptions.GROUP_CALL
                                else "Private Call"
                            )
                            contact_id = elem.info_dmr.ts2_default_tg.id
                        data_with_ts = current_data.copy() | {
                            "name": f"{elem.callsign} {ts}",
                            "contact": contact,
                            "contact_call_type": contact_call_type,
                            "contact_id": contact_id,
                            "color_code": color_code,
                            "slot": f"{ts_n}",
                        }
                        self.data[key].append(data_with_ts)
                else:
                    raise ValueError(f"Unknown key: {key}")
