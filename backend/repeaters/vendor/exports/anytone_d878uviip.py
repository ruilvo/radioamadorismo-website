"""
Module to generate the files part of the CSV export for the D878UVII+.

On the Anytone D878UVII+, names are limited to 16 chars.
"""

import io
import csv


from django.db.models import Q

from repeaters.models import (
    DimLocation,
    DimRf,
    DimFm,
    DimDmrTg,
    FactRepeater,
)


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
# Channel.CSV  -> Done
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
# Zone.CSV -> Done
# codeplug.LST  -> Not needed


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


class DimDmrTgAnytoneUVIIPlusSerializer:  # pylint: disable=too-few-public-methods
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


class ReceiveGroupsAnytoneUVIIPlusSerializer:  # pylint: disable=too-few-public-methods
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


class ChannelAnytoneUVIIPlusSerializer:  # pylint: disable=too-few-public-methods
    """
    Generates `Channel.csv` as a StringIO.
    """

    def __init__(self):  # pylint: disable=too-many-locals
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
                    ctcss = "Off"
                    if elem.info_fm.tone:
                        ctcss = f"{elem.info_fm.tone:.1f}"
                    current_data |= {
                        "no": f"{count}",
                        "name": elem.callsign,
                        "bw": bw,
                        "ctcss": ctcss,
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
                            count += 1  # Needs an extra tick of the counter
                            contact = elem.info_dmr.ts2_default_tg.name
                            contact_call_type = (
                                "Group Call"
                                if elem.info_dmr.ts2_default_tg.call_mode
                                == DimDmrTg.CallModeOptions.GROUP_CALL
                                else "Private Call"
                            )
                            contact_id = elem.info_dmr.ts2_default_tg.id
                        data_with_ts = current_data.copy() | {
                            "no": f"{count}",
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

        for key, data in self.data.items():
            for elem in data:
                if "fm" in key:
                    # Write data for FM repeaters
                    writer.writerow(
                        [
                            elem["no"],  # No.
                            elem["name"],  # Channel Name
                            elem["rx"],  # Receive Frequency
                            elem["tx"],  # Transmit Frequency
                            "A-Analog",  # Channel Type
                            "High",  # Transmit Power
                            elem["bw"],  # Band Width
                            "Off",  # CTCSS/DCS Decode
                            elem["ctcss"],  # CTCSS/DCS Encode
                            "Portugal",  # Contact
                            "Group Call",  # Contact Call Type
                            "268",  # Contact TG/DMR ID
                            "CT0ZZZ",  # Radio ID
                            "Off",  # Busy Lock/TX Permit
                            "Carrier",  # Squelch Mode
                            "Off",  # Optional Signal
                            "1",  # DTMF ID
                            "1",  # 2Tone ID
                            "1",  # 5Tone ID
                            "Off",  # PTT ID
                            "1",  # Color Code
                            "1",  # Slot
                            "None",  # Scan List
                            "None",  # Receive Group List
                            "Off",  # PTT Prohibit
                            "Off",  # Reverse
                            "Off",  # Simplex TDMA
                            "Off",  # Slot Suit
                            "Normal Encryption",  # AES Digital Encryption
                            "Off",  # Digital Encryption
                            "Off",  # Call Confirmation
                            "Off",  # Talk Around(Simplex)
                            "Off",  # Work Alone
                            "251.1",  # Custom CTCSS
                            "1",  # 2TONE Decode
                            "Off",  # Ranging
                            "On",  # Through Mode
                            "Off",  # APRS RX
                            "Off",  # Analog APRS PTT Mode
                            "Off",  # Digital APRS PTT Mode
                            "Off",  # APRS Report Type
                            "1",  # Digital APRS Report Channel
                            "0",  # Correct Frequency[Hz]
                            "Off",  # SMS Confirmation
                            "0",  # Exclude channel from roaming
                            "0",  # DMR MODE
                            "0",  # DataACK Disable
                            "0",  # R5toneBot
                            "0",  # R5ToneEot
                            "0",  # Auto Scan
                            "0",  # Ana Aprs Mute
                            "0",  # Send Talker Alias
                        ]
                    )
                elif "dmr" in key:
                    # Write data for DMR repeaters
                    writer.writerow(
                        [
                            elem["no"],  # No.
                            elem["name"],  # Channel Name
                            elem["rx"],  # Receive Frequency
                            elem["tx"],  # Transmit Frequency
                            "D-Digital",  # Channel Type
                            "High",  # Transmit Power
                            "12.5K",  # Band Width
                            "Off",  # CTCSS/DCS Decode
                            "Off",  # CTCSS/DCS Encode
                            elem["contact"],  # Contact
                            elem["contact_call_type"],  # Contact Call Type
                            elem["contact_id"],  # Contact TG/DMR ID
                            "CT0ZZZ",  # Radio ID
                            "Off",  # Busy Lock/TX Permit
                            "Carrier",  # Squelch Mode
                            "Off",  # Optional Signal
                            "1",  # DTMF ID
                            "1",  # 2Tone ID
                            "1",  # 5Tone ID
                            "Off",  # PTT ID
                            elem["color_code"],  # Color Code
                            elem["slot"],  # Slot
                            "None",  # Scan List
                            "Todos TGs",  # Receive Group List
                            "Off",  # PTT Prohibit
                            "Off",  # Reverse
                            "Off",  # Simplex TDMA
                            "Off",  # Slot Suit
                            "Normal Encryption",  # AES Digital Encryption
                            "Off",  # Digital Encryption
                            "Off",  # Call Confirmation
                            "Off",  # Talk Around(Simplex)
                            "Off",  # Work Alone
                            "251.1",  # Custom CTCSS
                            "1",  # 2TONE Decode
                            "Off",  # Ranging
                            "On",  # Through Mode
                            "Off",  # APRS RX
                            "Off",  # Analog APRS PTT Mode
                            "Off",  # Digital APRS PTT Mode
                            "Off",  # APRS Report Type
                            "1",  # Digital APRS Report Channel
                            "0",  # Correct Frequency[Hz]
                            "Off",  # SMS Confirmation
                            "0",  # Exclude channel from roaming
                            "0",  # DMR MODE
                            "0",  # DataACK Disable
                            "0",  # R5toneBot
                            "0",  # R5ToneEot
                            "0",  # Auto Scan
                            "0",  # Ana Aprs Mute
                            "0",  # Send Talker Alias
                        ]
                    )

        return sio


class ZoneAnytoneUVIIPlusSerializer:  # pylint: disable=too-few-public-methods
    """
    Generates `Zone.csv` as a StringIO.
    """

    def __init__(self, channel_serializer: ChannelAnytoneUVIIPlusSerializer):
        """
        We shall make zones for PT, Madeira and Azores.
        Each zone will have a max of 16 channels.
        A different zone for each combination of FM/DMR 2m/70cm.
        """

        # Generate the data to be written to the CSV file
        raw_data = {}

        for zone_prefix, dict_name in [
            ("CPT 2m FM", "continent_2m_fm"),
            ("CPT 70cm FM", "continent_70cm_fm"),
            ("CPT 2m DMR", "continent_2m_dmr"),
            ("CPT 70cm DMR", "continent_70cm_dmr"),
            ("MDA 2m FM", "madeira_2m_fm"),
            ("MDA 70cm FM", "madeira_70cm_fm"),
            ("MDA 2m DMR", "madeira_2m_dmr"),
            ("MDA 70cm DMR", "madeira_70cm_dmr"),
            ("AZR 2m FM", "azores_2m_fm"),
            ("AZR 70cm FM", "azores_70cm_fm"),
            ("AZR 2m DMR", "azores_2m_dmr"),
            ("AZR 70cm DMR", "azores_70cm_dmr"),
        ]:
            count = 0

            for idx, elem in enumerate(channel_serializer.data[dict_name]):
                # Check whether we need to create a new zone (pt. 1)
                if idx % 16 == 0:
                    count += 1

                zone_name = f"{zone_prefix} {count}"

                # Check whether we need to create a new zone (pt. 2)
                if zone_name not in raw_data.keys():
                    raw_data[zone_name] = {
                        "members": [],
                        "rxs": [],
                        "txs": [],
                    }

                raw_data[zone_name]["members"].append(elem["name"])
                raw_data[zone_name]["rxs"].append(elem["rx"])
                raw_data[zone_name]["txs"].append(elem["tx"])

        self.data = {}
        for idx, (zone_name, zone_data) in enumerate(raw_data.items()):
            self.data[zone_name] = {
                "no": f"{idx+1}",
                "members": "|".join(zone_data["members"]),
                "rxs": "|".join(zone_data["rxs"]),
                "txs": "|".join(zone_data["txs"]),
                "a_chan": zone_data["members"][0],
                "a_rx": zone_data["rxs"][0],
                "a_tx": zone_data["txs"][0],
                "b_chan": zone_data["members"][0],
                "b_rx": zone_data["rxs"][0],
                "b_tx": zone_data["txs"][0],
            }

    def generate_csv(self) -> io.StringIO:
        """
        Generate the CSV file as a StringIO object.
        """

        sio = io.StringIO()
        writer = csv.writer(sio, dialect="d878uviiplus")

        header = [
            "No.",
            "Zone Name",
            "Zone Channel Member",
            "Zone Channel Member RX Frequency",
            "Zone Channel Member TX Frequency",
            "A Channel",
            "A Channel RX Frequency",
            "A Channel TX Frequency",
            "B Channel",
            "B Channel RX Frequency",
            "B Channel TX Frequency",
            "Zone Hide ",  # For some reason the trailing space is part of the name...
        ]
        writer.writerow(header)

        for zone_name, zone_data in self.data.items():
            writer.writerow(
                [
                    zone_data["no"],  # No.
                    zone_name,  # Zone Name
                    zone_data["members"],  # Zone Channel Member
                    zone_data["rxs"],  # Zone Channel Member RX Frequency
                    zone_data["txs"],  # Zone Channel Member TX Frequency
                    zone_data["a_chan"],  # A Channel
                    zone_data["a_rx"],  # A Channel RX Frequency
                    zone_data["a_tx"],  # A Channel TX Frequency
                    zone_data["b_chan"],  # B Channel
                    zone_data["b_rx"],  # B Channel RX Frequency
                    zone_data["b_tx"],  # B Channel TX Frequency
                    "0",  # Zone Hide
                ]
            )

        return sio
