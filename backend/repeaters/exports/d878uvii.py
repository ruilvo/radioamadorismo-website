"""
On the Anytone D878UVII, names are limited to 16 chars.
"""

import io
import csv

from typing import Tuple, List

from django.db.models import Q
from django.db.models.query import QuerySet

from repeaters.models import (
    DimDmr,
    DimDmrTg,
    FactRepeater,
)

from repeaters.utils import fix_dups


class Band2m:
    min = 144.0
    max = 146.0


class Band70cm:
    min = 430.0
    max = 440.0


class D878UVIIDialect(csv.excel):
    quotechar = '"'
    quoting = csv.QUOTE_ALL


csv.register_dialect("d878uvii", D878UVIIDialect)


def make_tg_names(qs: QuerySet) -> List[str]:
    names: List[str] = []
    elem: DimDmrTg
    for elem in qs:
        names.append(elem.name)

    names = fix_dups(names, sep=" ", start=1, update_first=True)
    names = [f"{name:.16}" for name in names]

    return names


def tgs_csv() -> io.StringIO:
    """
    Generates `TalkGroups.csv` as a StringIO object.
    """

    qs = DimDmrTg.objects.all()
    names = make_tg_names(qs)

    header = ["No.", "Radio ID", "Name", "Call Type", "Call Alert"]

    call_type_str = "Group Call"
    call_alert_str = "None"

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    idx: int
    item: DimDmrTg
    for idx, (item, name) in enumerate(zip(qs, names)):
        writer.writerow(
            [
                f"{idx+1}",
                f"{item.dmr_id}",
                name,
                call_type_str,
                call_alert_str,
            ]
        )

    return sio


def receive_groups_csv() -> io.StringIO:
    """
    Generates `ReceiveGroupCallList.csv` as a StringIO.

    We'll be generating 2 groups:
     - The expected TS1 slot TGs
     - All TGs
    """

    ts1_default_tgs_qs = DimDmrTg.objects.filter(
        dimdmr_ts1_default_tg__isnull=False
    ).distinct()
    ts1_alternative_tgs_qs = DimDmrTg.objects.filter(
        dimdmr_ts1_alternative_tgs__in=DimDmr.objects.all()
    ).distinct()

    ts1_tgs_qs = (ts1_default_tgs_qs | ts1_alternative_tgs_qs).distinct()
    tgs_qs = DimDmrTg.objects.all()
    ts1_tgs_mames = make_tg_names(ts1_tgs_qs)
    tgs_names = make_tg_names(tgs_qs)

    # RG's definition
    data_input = [
        ("TS1 Tipicos", ts1_tgs_qs, ts1_tgs_mames),
        ("Todos TGs", tgs_qs, tgs_names),
    ]

    data = []
    for name, qs, names in data_input:
        contact = "|".join(names)
        ids = "|".join(f"{tg.dmr_id}" for tg in qs)
        data.append((name, contact, ids))

    header = ["No.", "Group Name", "Contact", "Contact TG/DMR ID"]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    for idx, (name, contact, ids) in enumerate(data):
        writer.writerow(
            [
                f"{idx+1}",
                f"{name}",
                f"{contact}",
                f"{ids}",
            ]
        )

    return sio


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


def make_channel_qs() -> Tuple[QuerySet, QuerySet]:
    """
    Gets two sets of querysets, one with the FM information, another with the DMR
    information.
    """

    qs = FactRepeater.objects.all()

    qs_hd = qs.filter(info_half_duplex__isnull=False)
    qs_sp = qs.filter(info_simplex__isnull=False)

    # Rx between 144.0 and 146.0 OR between 430.0 and 440.0
    q_hd_rx_2m = Q(info_half_duplex__rx_mhz__gte=Band2m.min) & Q(
        info_half_duplex__rx_mhz__lte=Band2m.max
    )
    q_hd_rx_70cm = Q(info_half_duplex__rx_mhz__gte=Band70cm.min) & Q(
        info_half_duplex__rx_mhz__lte=Band70cm.max
    )
    q_hd_rx = q_hd_rx_2m | q_hd_rx_70cm
    # AND Tx between 144.0 and 146.0 OR between 430.0 and 440.0
    q_hd_tx_2m = Q(info_half_duplex__tx_mhz__gte=Band2m.min) & Q(
        info_half_duplex__tx_mhz__lte=Band2m.max
    )
    q_hd_tx_70cm = Q(info_half_duplex__tx_mhz__gte=Band70cm.min) & Q(
        info_half_duplex__tx_mhz__lte=Band70cm.max
    )
    q_hd_tx = q_hd_tx_2m | q_hd_tx_70cm
    # AND
    q_hd = q_hd_rx & q_hd_tx

    # For simplex it's just TRx between 144.0 and 146.0 OR between 430.0 and 440.0
    q_sp_2m = Q(info_simplex__freq_mhz__gte=Band2m.min) & Q(
        info_simplex__freq_mhz__lte=Band2m.max
    )
    q_sp_70cm = Q(info_simplex__freq_mhz__gte=Band70cm.min) & Q(
        info_simplex__freq_mhz__lte=Band70cm.max
    )
    q_sp = q_sp_2m | q_sp_70cm
    # And filter
    qs_hd = qs_hd.filter(q_hd)
    qs_sp = qs_sp.filter(q_sp)

    # Repeaters also need to have either FM or DMR information
    qs_hd_fm = qs_hd.filter(info_fm__isnull=False)
    qs_hd_dmr = qs_hd.filter(info_dmr__isnull=False)
    qs_sp_fm = qs_sp.filter(info_fm__isnull=False)
    qs_sp_dmr = qs_sp.filter(info_dmr__isnull=False)

    # Due to the way the DB is set, the 1750Hz tone is considered a "tone".
    # Let's filter for only standard tones.
    # This is just a dirty protection, in the future a list would be nice.
    cutoff = 500.0
    qs_hd_fm = qs_hd_fm.filter(info_fm__tone__lte=cutoff)
    qs_sp_fm = qs_sp_fm.filter(info_fm__tone__lte=cutoff)

    qs_fm = qs_hd_fm | qs_sp_fm
    qs_dmr = qs_hd_dmr | qs_sp_dmr

    return qs_fm, qs_dmr


def make_channel_names_fm(qs: QuerySet) -> List[str]:
    callsigns: List[str] = []
    elem: FactRepeater
    for elem in qs:
        callsigns.append(elem.callsign)

    callsigns = fix_dups(callsigns, sep=" ", start=1, update_first=True)

    return callsigns


def make_channel_names_dmr(qs: QuerySet) -> List[str]:
    callsigns: List[str] = []
    elem: FactRepeater
    for elem in qs:
        callsigns.append(elem.callsign)

    callsigns = fix_dups(callsigns, sep=" ", start=1, update_first=True)
    callsigns_ts1 = [callsign + " TS1" for callsign in callsigns]
    callsigns_ts2 = [callsign + " TS2" for callsign in callsigns]

    return callsigns_ts1, callsigns_ts2


def channel_csv() -> io.StringIO:
    """
    Generates a Channel.csv
    """

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

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    qs_fm, qs_dmr = make_channel_qs()
    callsigns_fm = make_channel_names_fm(qs_fm)
    callsigns_dmr_ts1, callsigns_dmr_ts2 = make_channel_names_dmr(qs_dmr)

    elem: FactRepeater
    count = 0
    # FM
    for elem, callsign in zip(qs_fm, callsigns_fm):
        count = count + 1
        rx_freq = (
            elem.info_half_duplex.tx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        tx_freq = (
            elem.info_half_duplex.rx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        writer.writerow(
            [
                f"{count}",  # No.
                callsign,  # Channel Name
                f"{rx_freq:.5f}",  # Receive Frequency
                f"{tx_freq:.5f}",  # Transmit Frequency
                "A-Analog",  # Channel Type
                "High",  # Transmit Power
                f'{"12.5K" if elem.info_fm.bandwidth=="NFM" else "25K"}',  # Band Width
                "Off",  # CTCSS/DCS Decode
                f"{elem.info_fm.tone:.1f}",  # CTCSS/DCS Encode
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
    # DMR
    for idx, elem in enumerate(qs_dmr):
        rx_freq = (
            elem.info_half_duplex.tx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        tx_freq = (
            elem.info_half_duplex.rx_mhz
            if elem.info_half_duplex != None
            else elem.info_simplex.freq_mhz
        )
        if elem.info_dmr.ts1_default_tg is not None:
            ts1_contact = elem.info_dmr.ts1_default_tg.name
            ts1_id = str(elem.info_dmr.ts1_default_tg.dmr_id)
        else:
            ts1_contact = "Portugal"
            ts1_id = "268"
        if elem.info_dmr.ts2_default_tg is not None:
            ts2_contact = elem.info_dmr.ts2_default_tg.name
            ts2_id = str(elem.info_dmr.ts2_default_tg.dmr_id)
        else:
            ts2_contact = "Local"
            ts2_id = "2"
        for ts_n, ts_contact, ts_id, rgl, callsigns_to_use in [
            ("1", ts1_contact, ts1_id, "TS1 Tipicos", callsigns_dmr_ts1),
            ("2", ts2_contact, ts2_id, "Todos TGs", callsigns_dmr_ts2),
        ]:
            count = count + 1
            writer.writerow(
                [
                    f"{count}",  # No.
                    callsigns_to_use[idx],  # Channel Name
                    f"{rx_freq:.5f}",  # Receive Frequency
                    f"{tx_freq:.5f}",  # Transmit Frequency
                    "D-Digital",  # Channel Type
                    "High",  # Transmit Power
                    "12.5K",  # Band Width
                    "Off",  # CTCSS/DCS Decode
                    "Off",  # CTCSS/DCS Encode
                    f"{ts_contact}",  # Contact
                    "Group Call",  # Contact Call Type
                    f"{ts_id}",  # Contact TG/DMR ID
                    "CT0ZZZ",  # Radio ID
                    "Always",  # Busy Lock/TX Permit
                    "Carrier",  # Squelch Mode
                    "Off",  # Optional Signal
                    "1",  # DTMF ID
                    "1",  # 2Tone ID
                    "1",  # 5Tone ID
                    "Off",  # PTT ID
                    f"{str(elem.info_dmr.color_code)}",  # Color Code
                    f"{ts_n}",  # Slot
                    "None",  # Scan List
                    f"{rgl}",  # Receive Group List
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
                    "1",  # DMR MODE
                    "0",  # DataACK Disable
                    "0",  # R5toneBot
                    "0",  # R5ToneEot
                    "0",  # Auto Scan
                    "0",  # Ana Aprs Mute
                    "0",  # Send Talker Alias
                ]
            )

    return sio


def zone_csv():
    """
    Generates a Zone.csv
    """

    qs_fm, qs_dmr = make_channel_qs()
    callsigns_fm = make_channel_names_fm(qs_fm)
    callsigns_dmr_ts1, callsigns_dmr_ts2 = make_channel_names_dmr(qs_dmr)

    initial_zones = {
        # Analogue VHF CPT
        "ana_vhf_cpt": {
            "name": "Ana VHF CPT",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "latitudes": [],
        },
        # Analogue UHF CPT
        "ana_uhf_cpt": {
            "name": "Ana UHF CPT",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "latitudes": [],
        },
        # DMR VHF CPT
        "dmr_vhf_cpt": {
            "name": "DMR VHF CPT",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "latitudes": [],
        },
        # DMR UHF CPT
        "dmr_uhf_cpt": {
            "name": "DMR UHF CPT",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "latitudes": [],
        },
        # Analogue VHF AZR
        "ana_vhf_azr": {
            "name": "Ana VHF AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # Analogue UHF AZR
        "ana_uhf_azr": {
            "name": "Ana UHF AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # DMR VHF AZR
        "dmr_vhf_azr": {
            "name": "DMR VHF AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # DMR UHF AZR
        "dmr_uhf_azr": {
            "name": "DMR UHF AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # Analogue VHF MDA
        "ana_vhf_mda": {
            "name": "Ana VHF MDA",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # Analogue UHF MDA
        "ana_uhf_mda": {
            "name": "Ana UHF MDA",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # DMR VHF MDA
        "dmr_vhf_mda": {
            "name": "DMR VHF MDA",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # DMR UHF MDA
        "dmr_uhf_mda": {
            "name": "DMR UHF MDA",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # Analogue XBand CPT
        "ana_xba_cpt": {
            "name": "Ana XBA CPT",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "latitudes": [],
        },
        # DMR XBand CPT
        "dmr_xba_cpt": {
            "name": "DMR XBA CPT",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "latitudes": [],
        },
        # Analogue XBand AZR
        "ana_xba_azr": {
            "name": "Ana XBA AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # DMR XBand AZR
        "dmr_xba_azr": {
            "name": "DMR XBA AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # Analogue XBand MDA
        "ana_xba_mda": {
            "name": "Ana XBA AZR",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # DMR XBand MDA
        "dmr_xba_mda": {
            "name": "DMR XBA MDA",
            "callsigns": [],
            "rx": [],
            "tx": [],
            "longitudes": [],
        },
        # Analogue NO LOC
        "ana_noloc": {
            "name": "Ana sem loc",
            "callsigns": [],
            "rx": [],
            "tx": [],
        },
        # DMR NO LOC
        "dmr_noloc": {
            "name": "DMR sem loc",
            "callsigns": [],
            "rx": [],
            "tx": [],
        },
    }

    # Buidld the initial zones for FM
    for elem, callsign in zip(qs_fm, callsigns_fm):
        # Do we know where it is?
        location = None
        latitude = None
        longitude = None
        if elem.info_location is not None:
            if (
                elem.info_location.latitude is not None
                and elem.info_location.longitude is not None
            ):
                location = elem.info_location.region
                latitude = elem.info_location.latitude
                longitude = elem.info_location.longitude
        assert (
            location is not None and latitude is not None and longitude is not None
        ) or (location is None)
        # Choose the right band
        band = None
        tx_freq = None
        rx_freq = None
        if elem.info_half_duplex is not None:
            # Repeater Tx is radio Rx and vice-versa
            tx_freq = elem.info_half_duplex.rx_mhz
            rx_freq = elem.info_half_duplex.tx_mhz
        elif elem.info_simplex is not None:
            tx_freq = elem.info_simplex.freq_mhz
            rx_freq = elem.info_simplex.freq_mhz
        if Band2m.min < tx_freq < Band2m.max and Band2m.min < rx_freq < Band2m.max:
            band = "2m"
        elif (
            Band70cm.min < tx_freq < Band70cm.max
            and Band70cm.min < rx_freq < Band70cm.max
        ):
            band = "70cm"
        else:
            band = "xba"
        # Now figure out the correct initial zone
        initial_zone = None
        coordinate_to_store = None
        if location is None:
            initial_zone = "ana_noloc"
        elif location == "CPT":
            coordinate_to_store = "latitude"
            if band == "2m":
                initial_zone = "ana_vhf_cpt"
            elif band == "70cm":
                initial_zone = "ana_uhf_cpt"
            elif band == "xba":
                initial_zone = "ana_xba_cpt"
        elif location == "AZR":
            coordinate_to_store = "longitude"
            if band == "2m":
                initial_zone = "ana_vhf_azr"
            elif band == "70cm":
                initial_zone = "ana_uhf_azr"
            elif band == "xba":
                initial_zone = "ana_xba_azr"
        elif location == "MDA":
            coordinate_to_store = "longitude"
            if band == "2m":
                initial_zone = "ana_vhf_mda"
            elif band == "70cm":
                initial_zone = "ana_uhf_mda"
            elif band == "xba":
                initial_zone = "ana_xba_mda"
        # And store in the right place
        initial_zones[initial_zone]["callsigns"].append(callsign)
        initial_zones[initial_zone]["rx"].append(rx_freq)
        initial_zones[initial_zone]["tx"].append(tx_freq)
        if coordinate_to_store == "latitude":
            initial_zones[initial_zone]["latitudes"].append(latitude)
        elif coordinate_to_store == "longitude":
            initial_zones[initial_zone]["longitudes"].append(longitude)
    # And we do the same for DMR
    for elem, callsign_ts1, callsign_ts2 in zip(
        qs_dmr, callsigns_dmr_ts1, callsigns_dmr_ts2
    ):
        # Do we know where it is?
        location = None
        latitude = None
        longitude = None
        if elem.info_location is not None:
            location = elem.info_location.region
            latitude = elem.info_location.latitude
            longitude = elem.info_location.longitude
        # Choose the right band
        band = None
        tx_freq = None
        rx_freq = None
        if elem.info_half_duplex is not None:
            # Repeater Tx is radio Rx and vice-versa
            tx_freq = elem.info_half_duplex.rx_mhz
            rx_freq = elem.info_half_duplex.tx_mhz
        elif elem.info_simplex is not None:
            tx_freq = elem.info_simplex.freq_mhz
            rx_freq = elem.info_simplex.freq_mhz
        if Band2m.min < tx_freq < Band2m.max and Band2m.min < rx_freq < Band2m.max:
            band = "2m"
        elif (
            Band70cm.min < tx_freq < Band70cm.max
            and Band70cm.min < rx_freq < Band70cm.max
        ):
            band = "70cm"
        else:
            band = "xba"
        # Now figure out the correct initial zone
        initial_zone = None
        coordinate_to_store = None
        if location is None:
            initial_zone = "dmr_noloc"
        elif location == "CPT":
            coordinate_to_store = "latitude"
            if band == "2m":
                initial_zone = "dmr_vhf_cpt"
            elif band == "70cm":
                initial_zone = "dmr_uhf_cpt"
            elif band == "xba":
                initial_zone = "dmr_xba_cpt"
        elif location == "AZR":
            coordinate_to_store = "longitude"
            if band == "2m":
                initial_zone = "dmr_vhf_azr"
            elif band == "70cm":
                initial_zone = "dmr_uhf_azr"
            elif band == "xba":
                initial_zone = "dmr_xba_azr"
        elif location == "MDA":
            coordinate_to_store = "longitude"
            if band == "2m":
                initial_zone = "dmr_vhf_mda"
            elif band == "70cm":
                initial_zone = "dmr_uhf_mda"
            elif band == "xba":
                initial_zone = "dmr_xba_mda"
        # And store in the right place
        for callsign in [callsign_ts1, callsign_ts2]:
            initial_zones[initial_zone]["callsigns"].append(callsign)
            initial_zones[initial_zone]["rx"].append(rx_freq)
            initial_zones[initial_zone]["tx"].append(tx_freq)
            if coordinate_to_store == "latitude":
                initial_zones[initial_zone]["latitudes"].append(latitude)
            elif coordinate_to_store == "longitude":
                initial_zones[initial_zone]["longitudes"].append(longitude)

    # Now we sort the zones
    for name in [
        "ana_vhf_cpt",
        "ana_uhf_cpt",
        "dmr_vhf_cpt",
        "dmr_uhf_cpt",
        "ana_xba_cpt",
        "dmr_xba_cpt",
    ]:
        # These sort by latitude
        for key in ["callsigns", "rx", "tx", "latitudes"]:
            zipped_lists = list(
                zip(initial_zones[name]["latitudes"], initial_zones[name][key])
            )
            sorted_lists = sorted(
                zipped_lists,
                key=lambda pair: pair[0],
                reverse=True,  # North to South
            )
            initial_zones[name][key] = [x for _, x in sorted_lists]
    for name in [
        "ana_vhf_azr",
        "ana_uhf_azr",
        "dmr_vhf_azr",
        "dmr_uhf_azr",
        "ana_vhf_mda",
        "ana_uhf_mda",
        "dmr_vhf_mda",
        "dmr_uhf_mda",
        "ana_xba_azr",
        "dmr_xba_azr",
        "ana_xba_mda",
        "dmr_xba_mda",
    ]:
        # These sort by longitude
        for key in ["callsigns", "rx", "tx", "longitudes"]:
            initial_zones[name][key] = [
                x
                for _, x in sorted(
                    zip(initial_zones[name]["longitudes"], initial_zones[name][key]),
                    key=lambda pair: pair[0],
                    reverse=False,  # East to West
                )
            ]

    # The AZR and MDA zones are fine, but we want to split each CPT zone into 3
    # N, C, S
    # So we get the number of callsigns and divide by 3 to get the number of channels per
    # zone. But for DMR we must round up to the nearest multiple of 2, so to not separate
    # TS1 and TS2 of the same repeater.

    zones = {}

    for name in ["ana_vhf_cpt", "ana_uhf_cpt", "dmr_vhf_cpt", "dmr_uhf_cpt"]:
        nchannels = len(initial_zones[name]["callsigns"])
        nchannels_per_zone = nchannels // 3
        if not nchannels_per_zone % 2 == 0:
            nchannels_per_zone += 1
        for suffix, idx in zip(
            ["N", "C", "S"], range(0, nchannels, nchannels_per_zone)
        ):
            zones[name + "_" + suffix.lower()] = {
                "name": initial_zones[name]["name"] + " " + suffix,
                "callsigns": initial_zones[name]["callsigns"][
                    idx : idx + nchannels_per_zone
                ],
                "rx": initial_zones[name]["rx"][idx : idx + nchannels_per_zone],
                "tx": initial_zones[name]["tx"][idx : idx + nchannels_per_zone],
            }

    for name in [
        "ana_vhf_azr",
        "ana_uhf_azr",
        "dmr_vhf_azr",
        "dmr_uhf_azr",
        "ana_vhf_mda",
        "ana_uhf_mda",
        "dmr_vhf_mda",
        "dmr_uhf_mda",
        "ana_xba_azr",
        "dmr_xba_azr",
        "ana_xba_mda",
        "dmr_xba_mda",
    ]:
        zones[name] = initial_zones[name]

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
        "Zone Hide ",  # For some reason the space is part of the name...
    ]

    sio = io.StringIO()
    writer = csv.writer(sio, dialect="d878uvii")
    writer.writerow(header)

    count = 0
    for idx, zone in enumerate(zones.values()):
        if len(zone["callsigns"]) == 0:
            continue
        count = count + 1
        writer.writerow(
            [
                f"{count}",  # No.
                zone["name"],  # Zone Name
                "|".join(zone["callsigns"]),  # Zone Channel Member
                "|".join(
                    [f"{item:.5f}" for item in zone["rx"]]
                ),  # Zone Channel Member RX Frequency
                "|".join(
                    [f"{item:.5f}" for item in zone["tx"]]
                ),  # Zone Channel Member TX Frequency
                zone["callsigns"][0],  # A Channel
                zone["rx"][0],  # A Channel RX Frequency
                zone["tx"][0],  # A Channel TX Frequency
                zone["callsigns"][0],  # B Channel
                zone["rx"][0],  # B Channel RX Frequency
                zone["tx"][0],  # B Channel TX Frequency
                "0",  # Zone Hide
            ]
        )

    return sio
